# /root/Smart-Parking-System/smart-parking-system-main/administration/urls.py
from django.urls import path
from .views import (
    AdminGarageStatsAPIView,
    AdminPaymentAnalyticsAPIView,
    AdminVehicleLogListAPIView,
    AdminSlotListCreateAPIView,
    AdminSlotDetailAPIView,
    AdminUserListAPIView,
    CreateAdminUserAPIView,
    AdminReservationListAPIView,
    admin_dashboard_view,
    ToggleUserActiveAPIView,
    AdminShiftListAPIView,
    AdminShiftReportAPIView,
)
from .views import operator_dashboard
from .views import entry_gate_view, exit_gate_view
from .views import OperationsLogAPIView
from .sse_views import dashboard_stream

urlpatterns = [
    path('', admin_dashboard_view, name='admin-dashboard'),
 # نظرة عامة وتحليلات
    path('stats/', AdminGarageStatsAPIView.as_view(), name='admin-stats'),
    path('analytics/', AdminPaymentAnalyticsAPIView.as_view(), name='admin-analytics'),

    path('logs/', AdminVehicleLogListAPIView.as_view(), name='admin-logs'),

    path('slots/', AdminSlotListCreateAPIView.as_view(), name='admin-slots'),
    path('slots/<int:pk>/', AdminSlotDetailAPIView.as_view(), name='admin-slot-detail'),

    path('users/', AdminUserListAPIView.as_view(), name='admin-users'),
    path('users/create-admin/', CreateAdminUserAPIView.as_view(), name='admin-create-admin'),
    path('users/<int:pk>/toggle-active/', ToggleUserActiveAPIView.as_view(), name='admin-toggle-user'),

    # الشفتات
    path('shifts/', AdminShiftListAPIView.as_view(), name='admin-shifts'),
    path('shifts/<int:pk>/report/', AdminShiftReportAPIView.as_view(), name='admin-shift-report'),

    path('reservations/', AdminReservationListAPIView.as_view(), name='admin-reservations'),

    path('operations/', OperationsLogAPIView.as_view(), name='operations-log'),

    path('dashboard/', operator_dashboard, name='operator-dashboard'),
    path('gate/exit/', exit_gate_view, name='exit-gate'),
    path('gate/entry/', entry_gate_view, name='entry-gate'),

    path('dashboard/stream/', dashboard_stream, name='dashboard-stream'),
]

