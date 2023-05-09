from .helpers import (
    get_user,
    get_all_users
)
from adminpanel_app.roles.helpers import (
    get_groups_from_ids,
    get_group_ids
)
from .serializers import (
    RegisterUserSerializer,
    LoginUserSerializer,
    UpdateLoginUserSerializer
)

from django.contrib.auth.hashers import make_password, check_password

# from rest_framework.authentication import SessionAuthentication, BasicAuthentication
# from drf_yasg.utils import swagger_auto_schema

from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions, SAFE_METHODS # type: ignore
from rest_framework.views import APIView # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework.status import ( # type: ignore
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_400_BAD_REQUEST
) 
# from django.contrib.auth.mixins import PermissionRequiredMixin
# from django.shortcuts import render


class UserDetailAPI(APIView):
    # permission_classes = [IsAuthenticated]#, DjangoModelPermissions]
    
    def get(self, request):
        """
            if user_slug is in request then fetch record for this  \n
            if user_slug not in request then fetch all user \n
            params -> {
                user_slug: [ string ] => optional
            }
        """
        slug = self.request.query_params.get('user_slug', None)
        if not slug:
            user_obj_list = get_all_users()
            if not user_obj_list:
                return Response(
                    {
                        'status': False,
                        'payload': user_obj_list,
                        'message': 'No Data'
                    },
                    HTTP_200_OK
                )
                
            return Response(
                {
                    'status': True,
                    'payload': user_obj_list,
                    'message': 'All Users Data Fetched'
                }, 
                HTTP_200_OK
            )

        user_obj = get_user(slug)
        if user_obj == None:
            return Response(
                {
                    'status': False,
                    'message': 'User Not Found'
                },
                HTTP_404_NOT_FOUND
            )

        serializer = LoginUserSerializer(user_obj)
        return Response(
            {
                'status': True,
                'payload': serializer.data,
                'message': f'User Data Fetched'
            },
            HTTP_200_OK
        )
            

    # @swagger_auto_schema(request_body=RegisterUserSerializer)
    def post(self, request):
        """
            to create user and assign roles to user \n
            body -> [
                email: [ string ]
                password: [ string ]
                username: [ string ]
                first_name: [ string ]
                last_name: [ string ]
                role_ids: [ list of int ] example [1, 3, 5]
            ]
        """
        role_ids = request.data.get('role_ids')
        if not role_ids:
            return Response(
                {
                    'status': False,
                    'message': f'role_ids is required'
                },
                HTTP_400_BAD_REQUEST
            )

        serializer = RegisterUserSerializer(data=request.data)
        if not serializer.is_valid():
            for key in serializer.errors.keys():
                return Response(
                    {
                        'status': False,
                        'message': serializer.errors.get(key)[0]
                    },
                    HTTP_400_BAD_REQUEST
                )
        
        serializer.validated_data['password'] = make_password(serializer.validated_data['password'])

        groups = get_groups_from_ids(role_ids)
        if not groups:
            return Response(
                {
                    'status': False,
                    'message': 'Role Not Found'
                },
                HTTP_404_NOT_FOUND
            )

        user = serializer.save()
        group_ids = get_group_ids(groups)
        user.groups.set(group_ids)
        return Response({'status': True, 'message': 'User is created'}, status=HTTP_200_OK)


    def put(self, request):
        """
            to update user details \n
            body -> {
                user_slug: [ string ]
                email: [ string ]
                password: [ string ]
                username: [ string ]
                first_name: [ string ]
                last_name: [ string ]
            }
        """
        slug = request.data.get('user_slug')
        if not slug:
            return Response({'status': False, 'message': 'Please Provide user_slug'}, HTTP_400_BAD_REQUEST)

        user_obj = get_user(slug)
        if user_obj == None:
            return Response({'status': False, 'message': 'User Not Found'}, HTTP_404_NOT_FOUND) 

        serializer = UpdateLoginUserSerializer(instance=user_obj, data=request.data)
        if not serializer.is_valid():
            for key in serializer.errors.keys():
                return Response({
                    'status': False,
                    'message': serializer.errors.get(key)[0]
                })

        serializer.save()
        return Response({'status': True, 'message': 'User Updated'}, HTTP_200_OK)


    def patch(self, request):
        """
            to change password \n
            body -> {
                user_slug: [ string ]
                password: [ string ]
                new_password: [ string ]
            }
        """

        slug = request.data.get('user_slug')
        if not slug:
            return Response({'status': False, 'message': 'Please Provide user_slug'}, HTTP_400_BAD_REQUEST)

        user_obj = get_user(slug)
        if user_obj == None:
            return Response({'status': False, 'message': 'User Not Found'}, HTTP_404_NOT_FOUND)

        password = request.data.get('password')
        if not password:
            return Response({'status': False, 'message': 'Please Provide password'}, HTTP_400_BAD_REQUEST)
        
        new_password = request.data.get("new_password")
        if not new_password:
            return Response({'status': False, 'message': 'Please Provide new_password'}, HTTP_400_BAD_REQUEST)
        elif not check_password(password, user_obj.password):
            return Response({'status': False, 'message': 'password not match'}, HTTP_400_BAD_REQUEST)

        user_obj.password = make_password(new_password)
        user_obj.save()
        return Response({'status': True, 'message': 'Password Changed'}, HTTP_200_OK)
    

    def delete(self, request):
        """
            to delete user \n
            params -> {
                user_slug: [ string ]
            }
        """
        slug = request.query_params.get('user_slug', None)
        if slug == None:
            return Response({'status': False, 'message': 'Please Provide user_slug'}, HTTP_404_NOT_FOUND)

        user = get_user(slug)
        if user == None:
            return Response({'status': False, 'message': 'User Not Found'}, HTTP_404_NOT_FOUND)

        user.delete()
        return Response({'status': True, 'message': 'User Deleted'}, HTTP_200_OK)


class UserRole(APIView):
    # permission_classes = [IsAuthenticated]

    def patch(self, request):
        """
            to change user roles \n
            body -> {
                user_slug: [ string ]
                role_ids: [ list of int ] => example [1, 3, 4]
            }
        """
        slug = request.data.get('user_slug')
        if not slug:
            return Response({'status': False, 'message': 'Please Provide user_slug'}, HTTP_400_BAD_REQUEST)

        user = get_user(slug)
        if user == None:
            return Response({'status': False, 'message': 'User Not Found'}, HTTP_404_NOT_FOUND)

        role_ids = request.data['role_ids']

        groups = get_groups_from_ids(role_ids)
        if not groups:
            return Response({'status': False, 'message': 'Roles Not Found'}, status=HTTP_404_NOT_FOUND)

        group_ids = get_group_ids(groups)
        user.groups.set(group_ids)
        return Response({'status': True, 'message': 'User Role Updated'}, HTTP_200_OK)