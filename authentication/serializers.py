from rest_framework import serializers
from authentication.models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length = 68, min_length = 6, write_only = True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


