from adminpanel_app.users.serializers import LoginUserSerializer

from django.contrib.auth import authenticate, login, logout

from rest_framework.views import APIView # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework.status import ( # type: ignore
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED,
)

from rest_framework_simplejwt.tokens import RefreshToken # type: ignore



class AuthAPI(APIView):
    def post(self, request):
        """
            authenticate a user to login \n
            body -> [
                email: [ string ]
                password: [ string ]
            ]
        """
        if request.user.is_authenticated:
            return Response({'status': False,'message': "You Are Already Logged in"})

        email = request.data.get('email', '').lower()
        password = request.data.get('password')

        user = authenticate(email=email, password=password)
        if not user:
            return Response({'status': False,'message': "Failed to Login"}, status=HTTP_401_UNAUTHORIZED)
        elif not user.is_superuser:
            return Response({'status': False,'message': "You Are Not Super Admin"}, status=HTTP_401_UNAUTHORIZED)

        login(request, user)
        refresh = RefreshToken.for_user(user)
        user_serializer = LoginUserSerializer(user)

        res = {
            'status': True,
            'token': str(refresh.access_token),
            'refreshToken': str(refresh),
            'payload': user_serializer.data,
            'message': "Login Successfully",
        }
        return Response(data=res, status=HTTP_200_OK)


    """ to logout login user """
    def get(self, request):
        logout(request)
        res = {'status': True,'message': "Logout Successfully"}
        return Response(data=res, status=HTTP_200_OK)