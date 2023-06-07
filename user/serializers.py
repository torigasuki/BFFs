from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User, Verify


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("email", "name", "password")
        extra_kwargs = {"password": {"write_only": True}}
        model = User

    def create(self, validated_data):
        # if Verify.objects.get(email=validated_data['email']).verify:
        #     user = User.objects.create_user(**validated_data)
        #     return user
        # else:
        #     raise serializers.ValidationError("이메일 인증을 완료 해주세요")
        user = User.objects.create_user(**validated_data)
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        token["name"] = user.name
        return token
