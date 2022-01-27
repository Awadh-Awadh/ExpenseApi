from django.template import exceptions
from jwt import DecodeError
from rest_framework import serializers
from authentication.models import CustomUser
from rest_framework.exceptions import AuthenticationFailed
from .renderers import AuthRender
from django.utils.encoding import smart_bytes, smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator



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

       

class SetPasswordSerializer(serializers.Serializer):
    password=serializers.CharField(min_length=6, max_length=68, write_only=True)
    uidb64=serializers.CharField(min_length=1, write_only=True)
    token=serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = "__all__"

    """
    validate function is called when is_valid function get invoked
    """
    def validate(self, attrs):

        """
        from the token, we decode it and and get the id. Using the id we can query the user and change that
        user's password with the new password
        """

        try:
            password = attrs.get("password")
            uidb64 = attrs.get("uidb64")
            token = attrs.get("token")
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(id=id)
            if not PasswordResetTokenGenerator.check_token(user, token):
                return AuthenticationFailed("Invalid token", 401)
            user.set_password(password)
            user.save()
            return user

        except DjangoUnicodeDecodeError:
             return AuthenticationFailed("Invalid token", 401)

        return super().validate(attrs)
