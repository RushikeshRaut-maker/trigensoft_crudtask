from ..serializer.Login_serilaizer import LoginSerializer
from utility.response import ApiResponse
from rest_framework.generics import GenericAPIView
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from utility.util import revoke_oauth_token



class LogoutView(GenericAPIView, ApiResponse):
    serializer_class = LoginSerializer
    authentication_classes = [OAuth2Authentication, ]


    def get(self, request, *args, **kwargs):
        try:
            # capture data
            response = revoke_oauth_token(request)
            return ApiResponse.response_ok(self, message="Logout successful", data=response)
        except Exception as e:
            return ApiResponse.response_internal_server_error(self, message=[str(e.args[0])])