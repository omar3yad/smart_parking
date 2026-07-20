from django.contrib import admin
from .models import EmployeeProfile, Shift

# تسجيل جدول EmployeeProfile في لوحة التحكم
@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone_number', 'is_active') # الحقول اللي هتظهر في الجدول برة
    list_filter = ('role', 'is_active') # فلاتر جانبية للبحث
    search_fields = ('user__username', 'user__first_name', 'phone_number') # خانة البحث

# تسجيل جدول Shift في لوحة التحكم
@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'start_time', 'end_time', 'actual_collected_cash', 'is_closed')
    list_filter = ('is_closed', 'start_time')
    search_fields = ('employee__username',)