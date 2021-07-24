from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import *
from rest_framework import status
from rest_framework.response import Response


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Accounts
        fields = ["id", "acc_name", "acc_phone", "acc_type", "acc_strength"]


class UserSerializer(serializers.ModelSerializer):

    class Meta:

        model = User
        fields = '__all__'

class ContactSerializer(serializers.ModelSerializer):

    class Meta:

        model = Contacts
        fields = '__all__'