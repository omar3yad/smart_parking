from django.db import models

# Create your models here.
# EmployeeProfile

# accounts/models.py (أو يمكنك وضعه في administration/models.py)
from django.db import models
from django.contrib.auth.models import User

class EmployeeProfile(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Administrator'),
        ('operator', 'Gate Operator / Cashier'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='operator')
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.get_role_display()})"


class Shift(models.Model):
    employee = models.ForeignKey(User, on_delete=models.PROTECT, related_name='shifts')
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    
    # المبالغ المالية لتقفيل الشفت باحترافية
    starting_cash = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, help_text="العهدة الافتتاحية في الدرج")
    expected_collected_cash = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, help_text="المبلغ المفترض تحصيله بناء على السيستم")
    actual_collected_cash = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="المبلغ الفعلي اللي الموظف سلمه")
    
    is_closed = models.BooleanField(default=False)

    def __str__(self):
        return f"Shift #{self.id} - {self.employee.username} ({'Closed' if self.is_closed else 'Active'})"