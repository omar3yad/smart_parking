from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .models import Shift
from .web_forms import EmployeeLoginForm, OpenShiftForm


class EmployeeLoginView(LoginView):
    template_name = "administration/login.html"
    authentication_form = EmployeeLoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("post-login-redirect")


class EmployeeLogoutView(LogoutView):
    next_page = reverse_lazy("employee-login")


@login_required
def post_login_redirect(request):
    has_active_shift = Shift.objects.filter(employee=request.user, is_closed=False).exists()
    if has_active_shift:
        return redirect("operator-dashboard")
    return redirect("open-shift-page")


@login_required
@ensure_csrf_cookie
def open_shift_page(request):
    active_shift = Shift.objects.filter(employee=request.user, is_closed=False).first()
    if active_shift:
        return redirect("operator-dashboard")
    return render(request, "administration/open_shift.html", {"form": OpenShiftForm()})