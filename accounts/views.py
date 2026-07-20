# /root/Smart-Parking-System/smart-parking-system-main/accounts/views.py
from .models import Shift
from django.db.models import Sum
from django.utils import timezone
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from .serializers import RegisterSerializer, UserSerializer
from .serializers import ShiftSerializer, CloseShiftSerializer

# 1. فيو التسجيل (Register)
class RegisterView(generics.CreateAPIView):
    """
    هذا الـ API يسمح للمستخدمين الجدد بإنشاء حساب.
    يستخدم الـ Serializer للتحقق من قوة كلمة المرور وتطابقها.
    """
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,) # مسموح للجميع بالوصول
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "user": UserSerializer(user).data,
                "message": "تم إنشاء الحساب بنجاح. يمكنك الآن تسجيل الدخول.",
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 2. فيو الملف الشخصي (Profile)
class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    هذا الـ API يسمح للمستخدم المسجل فقط برؤية وتعديل بياناته الشخصية.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated] # لا بد من وجود Token

    def get_object(self):
        return self.request.user

# 3. فيو التحقق من التوكن (اختياري - مفيد جداً للموبايل)
class CheckAuthView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        return Response({"status": "Authenticated", "user": request.user.username})

class OpenShiftView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # التأكد من عدم وجود شفت مفتوح لنفس الموظف حالياً
        active_shift = Shift.objects.filter(employee=request.user, is_closed=False).first()
        if active_shift:
            return Response({"error": "لديك شفت مفتوح بالفعل حالياً."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ShiftSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(employee=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CloseShiftView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        active_shift = Shift.objects.filter(employee=request.user, is_closed=False).first()
        if not active_shift:
            return Response({"error": "لا يوجد شفت مفتوح لإغلاقه."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = CloseShiftSerializer(data=request.data)
        if serializer.is_valid():
            # حساب إجمالي المبالغ المفترض تحصيلها من السيارات التي خرجت خلال هذا الشفت وتم دفعها
            total_collected = active_shift.exits_recorded.filter(is_paid=True).aggregate(total=Sum('total_fee'))['total'] or 0.00
            
            active_shift.end_time = timezone.now()
            active_shift.expected_collected_cash = total_collected
            active_shift.actual_collected_cash = serializer.validated_data['actual_collected_cash']
            active_shift.is_closed = True
            active_shift.save()
            
            return Response({
                "message": "تم إغلاق الشفت بنجاح",
                "expected_cash": active_shift.expected_collected_cash,
                "actual_cash": active_shift.actual_collected_cash,
                "difference": active_shift.actual_collected_cash - active_shift.expected_collected_cash
            }, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

