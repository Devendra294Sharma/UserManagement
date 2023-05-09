from .models import SidebarModule
from adminpanel_app.users.helpers import get_user
from .helpers import get_sidebar_which_have_perm
from adminpanel_app.permissions.helpers import get_model_view_perm_names

from rest_framework.views import APIView # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework.status import (HTTP_200_OK, HTTP_404_NOT_FOUND) # type: ignore


class SidebarAPI(APIView):
    def get(self, request):
        user_obj = get_user(request.user.slug)
        if user_obj == None:
            return Response({'status': False, 'message': 'User Not Found'}, HTTP_404_NOT_FOUND)
        
        sidebar_modules = SidebarModule.objects.all()
        sidebar = get_sidebar_which_have_perm(user_obj, sidebar_modules)
        return Response({'status': True, 'payload': sidebar, 'message': 'Sidebar'}, HTTP_200_OK)

        # model_permission_dict = get_model_view_perm_names()
        # sidebar = get_sidebar_which_have_perm(user_obj, model_permission_dict)
        # return Response({'status': True, 'payload': sidebar, 'message': 'Sidebar'}, HTTP_200_OK)