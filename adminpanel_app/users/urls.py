from django.urls import path
from .views import UserDetailAPI, UserRole

urlpatterns = [
    path('', UserDetailAPI.as_view(), name="user_detail"),
    path('/user-role', UserRole.as_view(), name="user_role"),
]