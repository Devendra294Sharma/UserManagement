from tokenize import group
from adminpanel_app import permissions
from adminpanel_app.permissions.helpers import sidebar_module_permission_dict_structure, sidebar_module_all_permission_dict_structure

from .serializers import GroupSerializer, GroupPermissionSerializer, AllGroupPermissionSerializer
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

def get_group(role_id):
    try:
        return Group.objects.get(id=role_id)
    except Group.DoesNotExist:
        return None

def get_groups_from_ids(role_ids):
    groups = Group.objects.filter(id__in=role_ids)
    serializer = GroupSerializer(instance=groups, many=True)
    return serializer.data

def get_group_ids(groups):
    group_ids = [d['id'] for d in groups]
    return group_ids

# def get_group_names(groups):
#     group_ids = [d['name'] for d in groups]
#     return group_ids

def get_all_group():
    groups = Group.objects.all()
    serializer = GroupSerializer(instance=groups, many=True)
    return serializer.data

def get_all_group_with_permission():
    groups = Group.objects.all()
    serializer = GroupPermissionSerializer(instance=groups, many=True)
    return serializer.data

def get_multiple_groups_permissions(group_data):
    for data in group_data:
        permissions = data.get('permissions')
        data['permissions'] = sidebar_module_permission_dict_structure(permissions)
    return group_data    

# ===============================================================

def get_all_permissions_of_groups():
    groups = Group.objects.all()
    serializer = AllGroupPermissionSerializer(instance=groups, many=True)
    return serializer.data

def get_multiple_groups_all_permissions(group_data):
    for data in group_data:
        group_id = data.get('id')
        permissions = data.get('permissions')
        data['permissions'] = sidebar_module_all_permission_dict_structure(permissions, group_id)
    return group_data     

