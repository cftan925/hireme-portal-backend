from rest_framework import serializers
from rest_framework.authtoken.views import Token
from .models import Profile, Chat, Notification, Freelancer, Booking, Service
from django.contrib.auth.models import User

class ProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = Profile
    fields = '__all__'
    depth = 3

class ChatSerializer(serializers.ModelSerializer):
  class Meta:
    model = Chat
    fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
  class Meta:
    model = Notification
    fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
  class Meta:
    model = Booking
    fields = '__all__'

class FreelancerSerializer(serializers.ModelSerializer):
  class Meta:
    model = Freelancer
    fields = '__all__'
    depth = 2

class ServiceSerializer(serializers.ModelSerializer):
  class Meta:
    model = Service
    fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email']
    depth = 1

    extra_kwargs = {'password': {
      'write_only': True,
      'required': True
    }}

  def create(self, validated_data):
    user = User.objects.create_user(**validated_data)
    Token.objects.create(user=user)
    return user