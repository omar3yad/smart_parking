# /root/Smart-Parking-System/smart-parking-system-main/accounts/views.py
from .models import Shift
from decimal import Decimal
from django.db.models import Sum
from django.utils import timezone
from parking.models import VehicleLog
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
        # تحقق إن مفيش أي شفت مفتوح خالص في الجراج (لأي موظف) - مش بس شفت الموظف الحالي
        any_active_shift = Shift.objects.filter(is_closed=False).first()
        if any_active_shift:
            if any_active_shift.employee_id == request.user.id:
                return Response({"error": "لديك شفت مفتوح بالفعل حالياً."}, status=status.HTTP_400_BAD_REQUEST)
            return Response({
                "error": f"يوجد شفت مفتوح حالياً للموظف '{any_active_shift.employee.username}'. "
                         f"لا يمكن فتح شفت جديد قبل إغلاقه."
            }, status=status.HTTP_400_BAD_REQUEST)

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
            actual_cash = serializer.validated_data['actual_collected_cash']

            total_collected = active_shift.exits_recorded.filter(is_paid=True).aggregate(
                total=Sum('total_fee')
            )['total'] or 0.00

            active_shift.end_time = timezone.now()
            active_shift.expected_collected_cash = total_collected
            active_shift.actual_collected_cash = actual_cash
            active_shift.is_closed = True
            active_shift.save()

            report = build_shift_report(active_shift, actual_cash=actual_cash)
            report["message"] = "تم إغلاق الشفت بنجاح"
            return Response(report, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def build_shift_report(shift, actual_cash=None):
    exits_qs = shift.exits_recorded.all().order_by('-exit_time')
    entries_qs = shift.entries_recorded.all()

    paid_exits = exits_qs.filter(is_paid=True)
    unpaid_exits = exits_qs.filter(is_paid=False)

    expected_cash = paid_exits.aggregate(total=Sum('total_fee'))['total'] or 0

    difference = None
    difference_status = None
    if actual_cash is not None:
        # ✅ حساب إجمالي المبلغ المفترض وجوده في الدرج (العهدة + الإيراد)
        total_expected_in_drawer = float(shift.starting_cash) + float(expected_cash)
        
        # ✅ حساب الفارق بناءً على إجمالي المبلغ بالدرج
        difference = float(actual_cash) - total_expected_in_drawer
        
        if difference > 0:
            difference_status = "زيادة"
        elif difference < 0:
            difference_status = "عجز"
        else:
            difference_status = "مطابق"

    return {
        "shift_id": shift.id,
        "employee": shift.employee.get_full_name() or shift.employee.username,
        "start_time": shift.start_time,
        "end_time": shift.end_time,
        "starting_cash": float(shift.starting_cash),
        "expected_collected_cash": float(expected_cash),
        "actual_collected_cash": float(actual_cash) if actual_cash is not None else None,
        "difference": abs(difference) if difference is not None else None,  # قيمة مطلقة للعرض
        "difference_status": difference_status,
        "cars_entered_count": entries_qs.count(),
        "cars_exited_count": exits_qs.count(),
        "cars_exited_paid_count": paid_exits.count(),
        "cars_exited_unpaid_count": unpaid_exits.count(),
        "unpaid_warning": (
            f"⚠️ يوجد {unpaid_exits.count()} سيارة خرجت ولم يتم تأكيد دفعها بعد!"
            if unpaid_exits.exists() else None
        ),
        "exits_detail": [
            {
                "license_plate": e.license_plate,
                "entry_time": e.entry_time,
                "exit_time": e.exit_time,
                "total_fee": float(e.total_fee),
                "is_paid": e.is_paid,
            }
            for e in exits_qs
        ],
    }

class ShiftSummaryView(APIView):
    """معاينة حية لبيانات الشفت المفتوح - قبل الإغلاق"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        active_shift = Shift.objects.filter(employee=request.user, is_closed=False).first()
        if not active_shift:
            return Response({"error": "لا يوجد شفت مفتوح حالياً."}, status=status.HTTP_404_NOT_FOUND)
        return Response(build_shift_report(active_shift))