from django.urls import path
from .views import SidebarAPI

urlpatterns = [
    path('', SidebarAPI.as_view(), name="sidebar"),
]