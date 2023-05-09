from dataclasses import field
from pyexpat import model
from adminpanel_app.permissions.serializers import PermissionSerializer, AllPermissionSerializer

from django.contrib.auth.models import Group, Permission

from rest_framework.serializers import ModelSerializer, SerializerMethodField # type: ignore

class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class GroupPermissionSerializer(ModelSerializer):
    permissions = SerializerMethodField()
    # PermissionSerializer
    class Meta:
        model = Group
        fields = [
            'id',
            'name',
            'permissions'
        ]
    
    def get_permissions(self, instance):
        return PermissionSerializer(instance.permissions, many=True).data

class GroupNameSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']


class AllGroupPermissionSerializer(ModelSerializer):
    permissions = SerializerMethodField()
    # PermissionSerializer
    class Meta:
        model = Group
        fields = [
            'id',
            'name',
            'permissions'
        ]
    
    def get_permissions(self, instance):
        permissions = Permission.objects.filter(content_type_id__model__in = ["user" , "permission" , "group"])
        return AllPermissionSerializer(permissions, many=True).data

        