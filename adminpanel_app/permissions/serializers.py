from django.contrib.auth.models import Permission

from rest_framework.serializers import ModelSerializer, SerializerMethodField # type: ignore


class PermissionSerializer(ModelSerializer):
    model_name = SerializerMethodField()

    class Meta:
        model = Permission
        fields = [
            'id',
            'name',
            'codename',
            'model_name'
        ]

    def get_model_name(self, instance):
        return instance.content_type.model

class AllPermissionSerializer(ModelSerializer):
    model_name = SerializerMethodField()

    class Meta:
        model = Permission
        fields = [
            'id',
            'name',
            'codename',
            'model_name'
        ]

    def get_model_name(self, instance):
        return instance.content_type.model        

