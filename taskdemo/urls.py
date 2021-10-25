"""taskdemo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from task_app.views.admin_view import Admin_view
from task_app.views.user_access import User_access_view
from task_app.views.login import Loginviewset
from task_app.views.logout import LogoutView
from django.conf.urls import url

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('task_app',include('task_app.url')),
]




urlpatterns +=[
	url(r'^admin/$',Admin_view.as_view({'get':'list'})),
	url(r'^admin/(?P<id>.+)/$',Admin_view.as_view({'get': 'retrieve', 'put': 'partial_update','delete':'delete'})),


]

urlpatterns +=[
	url(r'^user_access/(?P<id>.+)/$',User_access_view.as_view({'get':'give_access'}))

]


