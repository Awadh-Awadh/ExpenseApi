import pdb
from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from authentication.models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length = 68, min_length = 6, write_only = True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class EmailVerifySerializer(serializers.ModelSerializer):
        token = serializers.CharField(max_length=555)

        class Meta:
                model = CustomUser
                fields = ['token']

class LoginSerializer(serializers.ModelSerializer):
    password=serializers.CharField(max_length=68, min_length=6, write_only=True)
    class Meta:
        model= CustomUser
        fields = ['email', 'password', 'tokens', 'username']
        read_only_fields=('tokens', 'username')


class RequestPasswordResetEmailSerializer(serializers.Serializer):
        email = serializers.EmailField(min_length=2)

        class Meta:
            fields=["email"]

        def validate(self, attrs):

            try:
                pass
            except Exception as e:
                pass

            return super().validate(attrs)