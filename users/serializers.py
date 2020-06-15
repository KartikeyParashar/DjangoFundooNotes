from .models import Fundoo, SendMessage
from rest_framework import serializers


class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Fundoo
        fields = ['username', 'email', 'password']


class LoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = Fundoo
        fields = ['username', 'password']


class ResetPasswordSerializer(serializers.ModelSerializer):

    class Meta:
        model = Fundoo
        fields = ['username', 'email']


class ForgotPasswordSerializer(serializers.ModelSerializer):

    password = serializers.CharField(min_length=8, write_only=True)
    confirm_password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = Fundoo
        fields = ['password', 'confirm_password']


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Fundoo
        fields = ['upload']


class PhoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = SendMessage
        fields = '__all__'
