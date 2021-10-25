from rest_framework import serializers
from ..models import UserAccess


class User_Access_Serializer(serializers.ModelSerializer):

	class Meta:
		model=UserAccess
		fields='__all__'


