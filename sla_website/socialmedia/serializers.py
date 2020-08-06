'''from rest_framework import serializers
from .models import Acts, Post, CustomUser
from django.contrib.auth import get_user_model


CustomUser = get_user_model()

class UserSerializer(serializers.Serializer):
	class Meta:
		model = CustomUser
		fields = '__all__'

	def create(self, validated_data):
		user = CustomUser.objects.create_user(
				username = validated_data['username'],
				password = validated_data['password'],
			)

		return user'''
    