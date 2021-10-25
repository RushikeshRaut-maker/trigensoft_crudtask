#from django.shortcuts import render
from django.shortcuts import render
from rest_framework import viewsets,permissions
from rest_framework.generics import GenericAPIView
from ..serializer.Login_serilaizer import LoginSerializer
from ..models import Users 
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from utility.util import EmailorUsername,generate_token,get_login_response
from utility.response import ApiResponse

class Loginviewset(GenericAPIView,EmailorUsername,ApiResponse):

	serializer_class = LoginSerializer

	def post(self,request,*args,**kwargs):

		try:
			host= request.get_host()
			email=request.data.get('email')
			password=request.data.get('password')


			if not email or not password:
				#return Response(self,status=400)
				return ApiResponse.response_bad_request(self,message='username and password required')

			user =EmailorUsername.authenticate(self,username=email,password=password)
			print("login user==",user)

			if user:

				token=generate_token(request,user)

				if token:

						resp_dict=get_login_response(user,token)
						resp_dict['token']=token
						return ApiResponse.response_ok(self,data=resp_dict,message='Login Successful')

				else:
					return ApiResponse.response_bad_request(self,message='User Not Authenticate')

			else:
				return ApiResponse.response_unauthorized(self,message='Username And Password Incorrect')
		except Exception as e:
				return ApiResponse.response_internal_server_error(self, message=[str(e.args[0])])
				
