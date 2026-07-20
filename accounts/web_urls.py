from django.urls import path
from .web_views import EmployeeLoginView, EmployeeLogoutView, post_login_redirect, open_shift_page

urlpatterns = [
    path("login/", EmployeeLoginView.as_view(), name="employee-login"),
    path("logout/", EmployeeLogoutView.as_view(), name="employee-logout"),
    path("redirect/", post_login_redirect, name="post-login-redirect"),
    path("shift/open-page/", open_shift_page, name="open-shift-page"),
]