from adminpanel_app.permissions.helpers import (
    get_permission_ids,
    sidebar_module_permission_dict_structure,
    sidebar_module_all_permission_dict_structure
)
from .helpers import (
    get_group,
    get_all_group,
    get_all_group_with_permission,
    get_multiple_groups_permissions,
    get_all_permissions_of_groups,
    get_multiple_groups_all_permissions
)
from .serializers import (
    GroupSerializer,
    GroupNameSerializer,
    GroupPermissionSerializer,
    AllGroupPermissionSerializer
)

# from rest_framework import generics
# from django.contrib.auth.mixins import PermissionRequiredMixin
from rest_framework.permissions import IsAuthenticated # type: ignore
from rest_framework.views import APIView # type: ignore 
from rest_framework.response import Response # type: ignore
from rest_framework.status import ( # type: ignore
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_400_BAD_REQUEST
)


class RoleDetailAPI(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        """
            if role_id is in request then fetch role for this id \n
            if role_id not in request then fetch all role \n
            params -> {
                role_id: [ int ] => optional
            }
        """
        role_id = self.request.query_params.get('role_id', None)
        if not role_id:
            group_obj_list = get_all_group()
            print(group_obj_list, )
            if not group_obj_list:
                return Response(
                    {
                        'status': False,
                        'payload': group_obj_list,
                        'message': 'No Data'
                    }, 
                    HTTP_404_NOT_FOUND
                )

            return Response(
                {
                    'status': True,
                    'payload': group_obj_list,
                    'message': 'All Role Fetched'
                }, 
                HTTP_200_OK
            )

        group_obj = get_group(role_id)
        if group_obj == None:
            return Response({'status': False, 'message': 'Role Not Found'}, HTTP_404_NOT_FOUND)

        serializer = GroupSerializer(group_obj)
        return Response({'status': True, 'payload': serializer.data, 'message': f'Role Data Fetched'}, HTTP_200_OK)


    def post(self, request):
        """
            create role

            body -> {
                name: [ string ]
            }
        """
        serializer = GroupNameSerializer(data=request.data)
        if not serializer.is_valid():
            if "name" in serializer.errors:
                return Response({'status': False, 'message': serializer.errors.get('name')[0]})
        serializer.validated_data['name'] = serializer.validated_data['name'].upper()
        serializer.save()
        return Response({'status': True, 'message': 'Role is Created'}, HTTP_200_OK)


    def put(self, request):
        """
            change role name

            body -> {
                role_id: [ int ]
                name: [ string ]
            }
        """
        role_id = request.data.get('role_id')
        name = request.data.get('name')
        
        if not role_id:
            return Response({'status': False, 'message': 'Please Provide role_id'}, HTTP_400_BAD_REQUEST)
        elif not name:
            return Response({'status': False, 'message': 'Please Provide role name'}, HTTP_400_BAD_REQUEST)

        group_obj = get_group(role_id)
        if group_obj == None:
            return Response({'status': False, 'message': 'Role Not Found'}, HTTP_404_NOT_FOUND) 

        serializer = GroupNameSerializer(instance=group_obj, data={'name': name})
        if not serializer.is_valid():
            if "name" in serializer.errors:
                return Response({'status': False, 'message': serializer.errors.get('name')[0]})

        serializer.validated_data['name'] = serializer.validated_data['name'].upper()
        serializer.save()
        return Response({'status': True, 'message': 'Role Updated'}, HTTP_200_OK)


    def delete(self, request):
        """
            delete role 

            params -> {
                role_id: [ int ]
            }
        """
        role_id = request.query_params.get('role_id', None)
        if role_id == None:
            return Response({'status': False, 'message': 'Please Provide role_id'}, HTTP_404_NOT_FOUND)

        group = get_group(role_id)
        if group == None:
            return Response({'status': False, 'message': 'Role Not Found'}, HTTP_404_NOT_FOUND)

        group.delete()
        return Response({'status': True, 'message': 'Role Deleted'}, HTTP_200_OK)


class RolePermissionAPI(APIView):
    def get(self, request):
        """
            get role data with its permission \n
            if role_id is in request then fetch role for specific role_id if not then fetch all role \n
            params -> {
                role_id: [ int ] => optional
            }
        """
        role_id = self.request.query_params.get('role_id', None)
        if not role_id:
            group_obj_list = get_all_group_with_permission()
            if not group_obj_list:
                return Response(
                    {
                        'status': False,
                        'payload': group_obj_list,
                        'message': 'No Data'
                    }, 
                    HTTP_404_NOT_FOUND
                )

            get_multiple_groups_permissions(group_obj_list)
            return Response(
                {
                    'status': True,
                    'payload': group_obj_list,
                    'message': 'All Role Fetched'
                }, 
                HTTP_200_OK
            )

        group_obj = get_group(role_id)
        if group_obj == None:
            return Response({'status': False, 'message': 'Role Not Found'}, HTTP_404_NOT_FOUND)

        serializer = GroupPermissionSerializer(group_obj)
        payload = serializer.data
        payload['permissions'] = sidebar_module_permission_dict_structure(payload.get('permissions'))
        return Response({'status': True, 'payload': payload, 'message': 'Role Data Fetched'}, HTTP_200_OK)


    def post(self, request):
        """
            body -> [
                role_id: [ int ]
                permission_ids: [ list of int ]
            ]
        """
        role_id = request.data.get('role_id')
        permission_ids = request.data.get('permission_ids')

        if not role_id:
            return Response({'status': False, 'message': f'role_id is required'}, HTTP_400_BAD_REQUEST)
        elif type(role_id) is not int:
            return Response({'status': False, 'message': f'role_id must be integer'}, HTTP_400_BAD_REQUEST)
        elif not permission_ids:
            return Response({'status': False, 'message': f'permission_ids is required'}, HTTP_400_BAD_REQUEST)

        group = get_group(role_id)
        if not group:
            return Response({'status': False, 'message': 'Role Not Found'}, HTTP_404_NOT_FOUND)

        permission_id_list = get_permission_ids(permission_ids)
        group.permissions.set(permission_id_list)
        return Response({'status': True, 'message': 'Permissions Assigned to Role'}, HTTP_200_OK)


class RoleAllPermissionAPI(APIView):
    def get(self, request):
        """
            get role data with its permission \n
            if role_id is in request then fetch role for specific role_id if not then fetch all role \n
            params -> {
                role_id: [ int ] => optional
            }
        """
        role_id = self.request.query_params.get('role_id', None)
        if not role_id:
            group_obj_list = get_all_permissions_of_groups()
            if not group_obj_list:
                return Response(
                    {
                        'status': False,
                        'payload': group_obj_list,
                        'message': 'No Data'
                    }, 
                    HTTP_404_NOT_FOUND
                )

            get_multiple_groups_all_permissions(group_obj_list)
            return Response(
                {
                    'status': True,
                    'payload': group_obj_list,
                    'message': 'All Role Fetched'
                }, 
                HTTP_200_OK
            )

        group_obj = get_group(role_id)
        if group_obj == None:
            return Response({'status': False, 'message': 'Role Not Found'}, HTTP_404_NOT_FOUND)

        serializer = AllGroupPermissionSerializer(group_obj)
        payload = serializer.data
        payload['permissions'] = sidebar_module_all_permission_dict_structure(payload.get('permissions'), group_obj.id)
        return Response({'status': True, 'payload': payload, 'message': 'Role Data Fetched'}, HTTP_200_OK)


    def post(self, request):
        """
            body -> [
                role_id: [ int ]
                permission_ids: [ list of int ]
            ]
        """
        role_id = request.data.get('role_id')
        permission_ids = request.data.get('permission_ids')

        if not role_id:
            return Response({'status': False, 'message': f'role_id is required'}, HTTP_400_BAD_REQUEST)
        elif type(role_id) is not int:
            return Response({'status': False, 'message': f'role_id must be integer'}, HTTP_400_BAD_REQUEST)
        elif not permission_ids:
            return Response({'status': False, 'message': f'permission_ids is required'}, HTTP_400_BAD_REQUEST)

        group = get_group(role_id)
        if not group:
            return Response({'status': False, 'message': 'Role Not Found'}, HTTP_404_NOT_FOUND)

        permission_id_list = get_permission_ids(permission_ids)
        group.permissions.set(permission_id_list)
        return Response({'status': True, 'message': 'Permissions Assigned to Role'}, HTTP_200_OK)
        



