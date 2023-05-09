from adminpanel_app.roles.serializers import GroupNameSerializer
from .models import User
from rest_framework.serializers import ModelSerializer, SerializerMethodField # type: ignore

class RegisterUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email',
            'password',
            'username',
            'first_name',
            'last_name'
        ]


class LoginUserSerializer(ModelSerializer):
    user_type = SerializerMethodField()
    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'first_name',
            'last_name',
            'slug',
            'is_superuser',
            'is_staff',
            'is_active',
            'user_type'
        ]

    def get_user_type(self, instance):
        if instance.is_superuser:
            return [{"name": "SUPER ADMIN"}]
        return GroupNameSerializer(instance.groups, many=True).data


class UpdateLoginUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'first_name',
            'last_name',
            'slug',
            'is_superuser',
            'is_staff',
            'is_active',
            'groups'
        ]