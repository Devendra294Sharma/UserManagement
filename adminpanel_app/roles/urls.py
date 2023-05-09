from django.urls import path
from .views import RoleDetailAPI, RolePermissionAPI, RoleAllPermissionAPI

urlpatterns = [
    path('', RoleDetailAPI.as_view(), name="role_detail"),
    path('/role-permission', RolePermissionAPI.as_view(), name="role-permission"),
    path('/role-all-permission', RoleAllPermissionAPI.as_view(), name="role-all-permission"),
]