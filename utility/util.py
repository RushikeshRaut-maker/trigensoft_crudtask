import requests
from task_app.models import Users
#from django.contrib.auth.models import auth_user
from oauth2_provider.settings import oauth2_settings
from oauth2_provider.models import Application,AccessToken,RefreshToken
from datetime import datetime,timedelta
from django.conf import settings
from oauthlib.oauth2.rfc6749.tokens import random_token_generator
from rest_framework.permissions import BasePermission
from .constant import *


class EmailorUsername(object):

	def authenticate(self,username=None,password=None):

		if '@' in username:
			kwargs ={'email':username}

		try:
			user=Users.objects.get(**kwargs)
			print("USER=",user)
			if user.check_password(password):
				return user
		except Users.DoesNotExist:
			print("exc==")
			return None



	def get_user(self,user_id):
		try:
			return Users.objects.get(pk=user_id)

		except Users.DoesNotExist:
			return None




def generate_token(request,user):

	print("In token generations")
	expire_secound = oauth2_settings.user_settings['ACCESS_TOKEN_EXPIRE_SECONDS']
	scopes=oauth2_settings.user_settings['SCOPES']
	
	application=Application.objects.first()
	expires =datetime.now() + timedelta(seconds=expire_secound)
	print("request",request)
	access_token=AccessToken.objects.create(
		user=user,
		application=application,
		token=random_token_generator(request),
		expires=expires,
		scope=scopes,
		)

	refresh_token=RefreshToken.objects.create(
		user=user,
		application=application,
		token= random_token_generator(request),
		access_token=access_token
		)

	token ={
		'access_token':access_token.token,
		'token_type':'Bearer',
		'expires_in':expire_secound,
		'refresh_token':refresh_token.token,
		'scope':scopes}
	return token


def get_login_response(user=None, token=None):
	resp_dict=dict()
	print("USERNEW",user)
	resp_dict['id']=user.id
	resp_dict['first_name']=user.first_name
	resp_dict['last_name']=user.last_name
	resp_dict['email']=user.email
	resp_dict['role_id']=user.role_id
	return resp_dict


def revoke_oauth_token(request):
	headers = {'Content-Type': 'application/x-www-form-urlencoded'}
	payload = {#'token': request.META['HTTP_AUTHORIZATION'][7:],
	       'token_type_hint': 'access_token',
	       }

	host = request.get_host()
	response = requests.post(settings.SERVER_PROTOCOLS + host + "/o/revoke_token/", data=payload,
	                     headers=headers)
	return response




class Is_Superadmin(BasePermission):
	def has_permission(self,request,view):
		return request.user.role_id == SUPERADMIN


def transform_list(self, data):
    return map(self.transform_single, data)



