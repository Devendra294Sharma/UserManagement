from .serializers import LoginUserSerializer
from .models import User

def get_user(user_slug):
    try:
        return User.objects.get(slug=user_slug)
    except User.DoesNotExist:
        return None

def get_all_users():
    users = User.objects.all()
    serializer = LoginUserSerializer(users, many=True)
    return serializer.data