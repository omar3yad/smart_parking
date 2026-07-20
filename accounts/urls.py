# /root/Smart-Parking-System/smart-parking-system-main/accounts/urls.py
from django.urls import path
from .views import RegisterView, UserProfileView, CheckAuthView
from .views import OpenShiftView, CloseShiftView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('check/', CheckAuthView.as_view(), name='check_auth'),
    path('shift/close/', CloseShiftView.as_view(), name='close-shift'),
    path('shift/open/', OpenShiftView.as_view(), name='open-shift'),
]