from rest_framework import serializers
from ..models import Users

class LoginSerializer(serializers.Serializer):

	class Meta:
		model=Users
		fields='__all__'