from djoser.serializers import UserCreateSerializer as B 
from rest_framework import serializers
from django.contrib.auth.models import User,Group

class UserCreateSerializer(B): # custom field for user creation form
    class Meta(B.Meta):
        fields = ['first_name','last_name','email','username','password']


class UserSerializer(serializers.ModelSerializer): # Serializer for user model related api
    class Meta:
        model = User
        fields = ['id','first_name','last_name','email','username','is_superuser']




        
        