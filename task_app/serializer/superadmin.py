from rest_framework import serializers
from ..models import Users

from utility.constant import *
from django.contrib.auth.models import Group


class User_serializer(serializers.ModelSerializer):
	confirm_password=serializers.CharField(max_length=256,write_only=True)

	class Meta:
		model=Users

		fields=[
			'role',
			'first_name',
			'last_name',
			'email',
			'is_staff',
			'is_active',
			'password',
			'confirm_password']

		extra_kwargs = {
            "email": {
                'allow_null': True, 'required': False,
                "error_messages": {
                    "invalid": "email should be valid",
                    "incorrect_type": "email should be valid",
                    "does_not_exist": "email already associated with another account",
                    "unique": "email already associated with another account",
                }
            },
        }
	def create(self,validate_data):
		if not validate_data.get('password') or not validate_data.get('confirm_password'):
			raise serializers.ValidationError('password and confirm_password required')

		if validate_data.get('password') != validate_data.get('confirm_password'):
			raise serializers.ValidationError('password and confirm_password are not match')
		validate_data.pop('confirm_password')

		return Users.objects.create(**validate_data)