from django.urls import path
from .views import PermissionDetailAPI

urlpatterns = [
    path('', PermissionDetailAPI.as_view(), name="permission_detail"),
]