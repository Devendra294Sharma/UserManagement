# from adminpanel_app.roles.helpers import get_group
from .helpers import (
    get_sidebar_model_permissions,
    get_all_sidebar_models_permissions,
    sidebar_module_permission_dict_structure,
)
from .serializers import PermissionSerializer

from rest_framework.views import APIView # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework.status import ( # type: ignore
    HTTP_200_OK,
    HTTP_404_NOT_FOUND
)


class PermissionDetailAPI(APIView):
    def get(self, request):
        """
            if sidebar_module_slug is in request then fetch permssions for this slug  \n
            if sidebar_module_slug not in request then fetch all permissions

            params -> {
                sidebar_module_slug: [ string ] => optional
            }
        """
        sidebar_module_slug = request.query_params.get('sidebar_module_slug', None)
        if not sidebar_module_slug:
            sidebar_models_permissions = get_all_sidebar_models_permissions()
            if not sidebar_models_permissions:
                 return Response(
                    {
                        'status': False,
                        'payload': sidebar_models_permissions,
                        'message': 'No Data'
                    },
                    HTTP_200_OK
                )
            sidebar = sidebar_module_permission_dict_structure(sidebar_models_permissions)
            return Response(
                {
                    'status': True,
                    'payload': sidebar,
                    'message': 'Sidebar All Permissions Fetched'
                },
                HTTP_200_OK
            )

        model_permissions = get_sidebar_model_permissions(sidebar_module_slug)
        if not model_permissions:
            return Response(
                {
                    'status': False,
                    'message': f'{sidebar_module_slug} Not Found'
                },
                HTTP_404_NOT_FOUND
            )

        serializer = PermissionSerializer(instance=model_permissions, many=True)
        sidebar_models_permissions = serializer.data
        sidebar = sidebar_module_permission_dict_structure(sidebar_models_permissions)
        return Response(
            {
                'status': True,
                'payload': sidebar,
                'message': f'{sidebar_module_slug} Permissions Data Fetched'
            },
            HTTP_200_OK
        )