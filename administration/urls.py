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
)
from .views import operator_dashboard
from .views import entry_gate_view, exit_gate_view
from .views import OperationsLogAPIView

urlpatterns = [
    path('', admin_dashboard_view,),
    path('stats/', AdminGarageStatsAPIView.as_view(), name='admin-stats'),
    path('analytics/', AdminPaymentAnalyticsAPIView.as_view(), name='admin-analytics'),
    path('logs/', AdminVehicleLogListAPIView.as_view(), name='admin-logs'),
    path('slots/', AdminSlotListCreateAPIView.as_view(), name='admin-slots'),
    path('slots/<int:pk>/', AdminSlotDetailAPIView.as_view(), name='admin-slot-detail'),
    path('users/', AdminUserListAPIView.as_view(), name='admin-users'),
    path('users/create-admin/', CreateAdminUserAPIView.as_view(), name='admin-create-admin'),
    path('reservations/', AdminReservationListAPIView.as_view(), name='admin-reservations'),
    path('dashboard/', operator_dashboard, name='operator-dashboard'),
    path('gate/exit/', exit_gate_view, name='exit-gate'),
    path('gate/entry/', entry_gate_view, name='entry-gate'),
    path('operations/', OperationsLogAPIView.as_view(), name='operations-log'),

]

urlpatterns += [
]