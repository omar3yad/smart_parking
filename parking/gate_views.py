# /root/Smart-Parking-System/smart-parking-system-main/parking/gate_views.py
from datetime import timedelta
from .models import VehicleLog
from django.utils import timezone
from accounts.models import Shift
from rest_framework.views import APIView
from core.redis_client import publish_event
from rest_framework.response import Response
from rest_framework import permissions, status
from .gate_serializers import GateEntrySerializer, GateExitSerializer
class RecentEntriesAPIView(APIView):
    """آخر سيارة داخلة خلال آخر دقيقتين - لبوابة الدخول"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        since = timezone.now() - timedelta(minutes=2)
        logs = VehicleLog.objects.filter(entry_time__gte=since).order_by('-entry_time')[:5]
        return Response(GateEntrySerializer(logs, many=True, context={'request': request}).data)


class PendingExitAPIView(APIView):
    """أول سيارة خرجت ولسه مدفوعة False - لبوابة الخروج"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        pending = VehicleLog.objects.filter(exit_time__isnull=False, is_paid=False).order_by('exit_time')
        current = pending.first()
        return Response({
            "current": GateExitSerializer(current, context={'request': request}).data if current else None,
            "queue_count": pending.count(),
        })


class ConfirmExitPaymentAPIView(APIView):
    """يضغطها الموظف بعد استلام الفلوس فعليًا"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            log = VehicleLog.objects.get(pk=pk, is_paid=False, exit_time__isnull=False)
        except VehicleLog.DoesNotExist:
            return Response({"error": "السجل غير موجود أو تم تأكيد دفعه مسبقًا."}, status=status.HTTP_404_NOT_FOUND)

        active_shift = Shift.objects.filter(is_closed=False).first()
        log.is_paid = True
        log.collected_by = request.user
        if not log.exit_shift and active_shift:
            log.exit_shift = active_shift
        log.save()
                # ── نشر الحدث لحظيًا على قناة الدفع ──
        publish_event('parking:payment', 'payment_confirmed', {
            "id": log.id,
            "license_plate": log.license_plate,
            "collected_by": request.user.username,
            "total_fee": float(log.total_fee),
        })
        return Response({"status": "success", "message": "تم تأكيد الدفع بنجاح."})

# ضيف الاستيرادات دي فوق الملف
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from .gate_serializers import VehicleLogFullSerializer


class GatePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


class EntriesHistoryAPIView(ListAPIView):
    """سجل كامل لكل السيارات الداخلة - مرتب من الأحدث - بـ Pagination"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = VehicleLogFullSerializer
    pagination_class = GatePagination

    def get_queryset(self):
        return VehicleLog.objects.all().order_by('-entry_time')

    def get_serializer_context(self):
        return {'request': self.request}


class ExitsHistoryAPIView(ListAPIView):
    """سجل كامل لكل السيارات الخارجة - مرتب من الأحدث - بـ Pagination"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = VehicleLogFullSerializer
    pagination_class = GatePagination

    def get_queryset(self):
        return VehicleLog.objects.filter(exit_time__isnull=False).order_by('-exit_time')

    def get_serializer_context(self):
        return {'request': self.request}