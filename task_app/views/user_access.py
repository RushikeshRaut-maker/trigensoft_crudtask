
from ..models import UserAccess
from ..serializer.user_access_serializer import User_Access_Serializer
from rest_framework.permissions import IsAuthenticated
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from utility.util import Is_Superadmin,transform_list
from utility.response import ApiResponse
from utility.constant import *


class User_access_view(GenericViewSet,
						mixins.ListModelMixin,
						mixins.CreateModelMixin,
						mixins.RetrieveModelMixin,
						mixins.UpdateModelMixin,
						ApiResponse):
		

		serilizer_class=User_Access_Serializer
		authentication_classes=[OAuth2Authentication]
		permission_classes =[IsAuthenticated,Is_Superadmin]


		def get_object(self,pk):
			try:
				return UserAccess.objects.select_related('user').get(pk=pk)
			except Exception as e:
				return ApiResponse.response_internal_server_error(self,message=[str(e.args)])
			


		def give_access(self,request,*args,**kwargs):

			try:
				get_id=self.kwargs.get('id')
				instance=self.get_object(get_id)
				print("Instance=",instance)
				if instance is None:
					return ApiResponse.response_bad_request(self,message="admin not found")

				instance.is_access=True
				instance.save()

				return ApiResponse.reponse_ok(self,message="accessed")
			except Exception as e:
				return ApiResponse.response_internal_server_error(self,message=[str(e.args)])
			


