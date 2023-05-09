from email.headerregistry import Group
from adminpanel_app.sidebar.helper_dicts import SIDEBAR_SLUG_AND_MODEL, SIDEBAR_MODEL_AND_MODULE
from .serializers import PermissionSerializer
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType


def get_sidebar_model_permissions(sidebar_module_slug):
    try:
        model_name = SIDEBAR_SLUG_AND_MODEL.get(sidebar_module_slug)
        content_type = ContentType.objects.get(model=model_name)
        return Permission.objects.filter(content_type=content_type)
    except ContentType.DoesNotExist:
        return None

def get_all_sidebar_models_permissions():
    models = SIDEBAR_SLUG_AND_MODEL.values()
    content_type = ContentType.objects.filter(model__in=models)
    permissions = Permission.objects.filter(content_type__in=content_type)
    serializer = PermissionSerializer(instance=permissions, many=True)
    return serializer.data

def sidebar_module_permission_dict_structure(permissions_data):
    module_permission_dict = {}
    for perm in permissions_data:
        module_name = ''
        permission_type = ''
        permission_id = ''

        for key in perm:
            if key == 'model_name':
                module_name = SIDEBAR_MODEL_AND_MODULE.get(perm[key])
            elif key == 'codename':
                # permission type => add, change, delete, view
                permission_type = perm[key].split('_')[0]
            elif key == 'id':
                permission_id = perm[key]

        # if module_name in module_permission_dict:
        #     module_permission_dict[module_name][permission_type] = permission_id
        # else:
        #     module_permission_dict[module_name] = {permission_type: permission_id}

        if module_name in module_permission_dict:
            module_permission_dict[module_name].append({permission_type: permission_id})
        else:
            module_permission_dict[module_name] = [{permission_type: permission_id}]

    return module_permission_dict


def sidebar_module_all_permission_dict_structure(permissions_data, group_id):
    module_permission_dict = {}
    for perm in permissions_data:
        print(perm, "-----------------------------PERM")
        module_name = ''
        permission_type = ''
        permission_id = ''

        for key in perm:
            if key == 'model_name':
                module_name = SIDEBAR_MODEL_AND_MODULE.get(perm[key])
            elif key == 'codename':
                # permission type => add, change, delete, view
                permission_type = perm[key].split('_')[0]
            elif key == 'id':
                permission_id = perm[key]

        # if module_name in module_permission_dict:
        #     module_permission_dict[module_name][permission_type] = permission_id
        # else:
        #     module_permission_dict[module_name] = {permission_type: permission_id}

        if module_name in module_permission_dict: 
            if Group.objects.filter(id=group_id, permissions__id=permission_id).exists():  
                module_permission_dict[module_name].append({permission_type: permission_id, "has_permission" : True})
            else:
                module_permission_dict[module_name].append({permission_type: permission_id, "has_permission" : False})

            
        else:
            print(module_permission_dict, "555555")
            if Group.objects.filter(id=group_id, permissions__id=permission_id).exists():
                module_permission_dict[module_name] = [{permission_type: permission_id, "has_permission" : True}]
            else:
                module_permission_dict[module_name] = [{permission_type: permission_id, "has_permission" : False}]


    return module_permission_dict


    
def get_permission_ids(permission_ids):
    return Permission.objects.filter(id__in=permission_ids).values_list('id', flat=True)

def get_model_view_perm_names(model_list):
    """
        return {model_name: app_label.view_model_name}
        for example -> {user: users.view_user}
    """
    models_list = SIDEBAR_MODEL_AND_MODULE.keys()
    app_and_model_names = ContentType.objects.filter(model__in=models_list)
    model_permission_dict = {}
    for app_and_model in app_and_model_names:
        model_permission_dict[app_and_model.model] = f'{app_and_model.app_label}.view_{app_and_model.model}'
    return model_permission_dict

# def get_model_view_perm_names():
#     """
#         return {model_name: app_label.view_model_name}
#         for example -> {user: users.view_user}
#     """
#     models_list = SIDEBAR_MODEL_AND_MODULE.keys()
#     app_and_model_names = ContentType.objects.filter(model__in=models_list)
#     model_permission_dict = {}
#     for app_and_model in app_and_model_names:
#         model_permission_dict[app_and_model.model] = f'{app_and_model.app_label}.view_{app_and_model.model}'
#     return model_permission_dict