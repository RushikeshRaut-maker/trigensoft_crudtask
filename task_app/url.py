from django.urls import path
from django.conf.urls import url
from task_app.views.login import Loginviewset
from task_app.views.logout import LogoutView
from task_app.views.admin_view import Admin_view
urlpatterns =[
	url('login/',Loginviewset.as_view()),
	url('logout/',LogoutView.as_view()),
	#url('admin/',Admin_view.as_view()),
	#url('admin_ref/<int:pk>/',Admin_view.as_view()),
]



