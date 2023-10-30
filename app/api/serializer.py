from app.models import *
from rest_framework import serializers
from django.contrib.auth.models import User
class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','email','password')
        extra_kwrgs = {'password': {'write_only':True}}

    def create(self,validated_data):
        user = User.objects.create_user(username=validated_data['username'],
                                        email= validated_data['email'],
                                        password=validated_data['password'])
        return user
    

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('user','name','locality','city','zipcode','state')        
