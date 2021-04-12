from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile
# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField()
    address = serializers.CharField()
    class Meta:
        model = User
        fields = ('id','phone_number','address', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['email'],email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        profile = Profile.objects.get(user=user)
        profile.phone_number = validated_data['phone_number']
        profile.address = validated_data['address']
        profile.save()
        return user

class ProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Profile
        fields = "__all__"

        depth = 1
        