from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import GenericViewSet
from ..serializer.superadmin import User_serializer
from utility.util import Is_Superadmin,transform_list
from utility.response import ApiResponse
from utility.constant import *
from ..models import Users
from rest_framework.permissions import IsAuthenticated
from oauth2_provider.contrib.rest_framework import OAuth2Authentication

class Admin_view(GenericViewSet,mixins.ListModelMixin,
				mixins.RetrieveModelMixin,
				mixins.CreateModelMixin,
				mixins.UpdateModelMixin,ApiResponse):

	authentication_classes = [OAuth2Authentication]
	permission_classes = [IsAuthenticated,Is_Superadmin]
	serializer_class= User_serializer
	def get_object(self,pk):
		try:
			print("Get_Object",pk)
			return Users.objects.get(pk=pk)
		except:
			return None

	def retrieve(self,request,**kwargs):
		try:
			print("retrieve")
			get_id=self.kwargs.get('id')

			instance=self.get_object(get_id)

			if instance is None:
				return ApiResponse.response_bad_request(self,message="admin not found")

			resp_dict=self.transform_single(instance)
			return ApiResponse.response_ok(self,data=resp_dict)
		except Exception as e:
			return ApiResponse.response_internal_server_error(self,message=[str(e.args)])


	def post(self,request,*args,**kwargs):
		try:
			data=request.data
			serializer=User_serializer(data=data)
			print("serializer==",serializer)
			if serializer.is_valid():
				print("Inside seralizer")
				serializer.save()
				print("Done save")

				user_instance=serializer.instance
				user_instance.set_password(data.get('password'))
				user_instance.save()
				resp_data=serializer.data
				return ApiResponse.response_created(self,data=resp_data,message="admin created")
			ser_error="Serializer_error"

			return ApiResponse.response_bad_request(self,message=ser_error)

		except Exception as e:
			return ApiResponse.response_internal_server_error(self,message=[str(e.args)])

	def list(self,request,*args,**kwargs):

		try:
			
			data=Users.objects.filter(role=ADMIN)

			resp_data=data
			
			response_data=transform_list(self,resp_data)
			return ApiResponse.response_ok(self,data=response_data)

		except Exception as e:
			return ApiResponse.response_internal_server_error(self,message=[str(e.args)])


	def update(self,request,*args,**kwargs):

		try:

			data=request.data
			get_id=self.kwargs.get('id')
			print("id==",get_id)
			instance =self.get_object(get_id)

			if instance is None:
				return ApiResponse.response_not_found(self,message='admin not found')

			serializer=User_serializer(instance,data=data,partial=True)
			if serializer.is_valid():
				serializer.save()

				response_data=serializer.data
				return ApiResponse.response_ok(self,data=response_data,message='admin successfully updated')

			ser_error="serializer_error"
			return ApiResponse.response_bad_request(self,message=ser_error)


		except Exception as e:
			return ApiResponse.response_internal_server_error(self,message=[str(e.args)])


	def delete(self,request,*args,**kwargs):

		try:
			get_id=self.kwargs.get('id')
			instance = self.get_object(get_id)

			if instance is None:
				return ApiResponse.response_bad_request(self,message="admin not found")
			instance.is_deleted=True
			instance.save()
			return ApiResponse.response_ok(self,message="admin successfully deleted")

		except Exception as e:
			return ApiResponse.response_internal_server_error(self,message=[str(e.args)])


	def transform_single(self, instance):
	    resp_dict = dict()
	    resp_dict['id'] = instance.id
	    resp_dict['first_name'] = instance.first_name
	    resp_dict['last_name'] = instance.last_name
	    resp_dict['email'] = instance.email
	    resp_dict['is_staff'] = instance.is_staff
	    
	    resp_dict['is_active'] = instance.is_active
	    resp_dict['role'] = instance.role_id
	    
	    return resp_dict
			









