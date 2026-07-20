from django import forms
from django.contrib.auth.forms import AuthenticationForm


class EmployeeLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="اسم المستخدم",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "اسم المستخدم", "autofocus": True})
    )
    password = forms.CharField(
        label="كلمة المرور",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "••••••••"})
    )
    error_messages = {
        "invalid_login": "اسم المستخدم أو كلمة المرور غير صحيحة.",
        "inactive": "هذا الحساب غير مفعّل.",
    }


class OpenShiftForm(forms.Form):
    starting_cash = forms.DecimalField(
        label="العهدة الافتتاحية (جنيه)",
        min_value=0, max_digits=10, decimal_places=2, initial=0,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "0.00"})
    )