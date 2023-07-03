from .models import ProfileUser, AvatarUser
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, update_session_auth_hash
from rest_framework.exceptions import ValidationError
from .utils import validate_password_user


class AuthUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(
            username=data.get("username", ""), password=data.get("password", "")
        )
        if not user:
            raise ValidationError("Неправильный логин или пароль.")
        return user


class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="first_name")

    class Meta:
        model = User
        fields = (
            "name",
            "username",
            "password",
        )


class AvatarUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvatarUser
        fields = (
            "src",
            "alt",
        )


class ProfileUserSerializer(serializers.ModelSerializer):
    avatar = AvatarUserSerializer(many=False, required=False)

    class Meta:
        model = ProfileUser
        fields = (
            "fullName",
            "email",
            "phone",
            "avatar",
        )


class ChangePasswordUserSerializer(serializers.Serializer):
    currentPassword = serializers.CharField()
    newPassword = serializers.CharField()

    def validate(self, data):
        validate_password_user(password=data.get("newPassword"))

        if data.get("newPassword") == data.get("currentPassword", ""):
            raise ValidationError("Пароли совпадают.")

        user = authenticate(
            username=self.context.get("request").user.username,
            password=data.get("currentPassword", ""),
        )
        if not user:
            raise ValidationError("Неверный пароль.")
        return data

    def save(self, **kwargs):
        user = self.context.get("request").user
        user.set_password(self.validated_data.get("newPassword"))
        user.save()
        update_session_auth_hash(self.context.get("request"), user)
