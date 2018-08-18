from django.conf.urls import url

from .views import (
	login,
	logout,
	account,
	change_password,
)

urlpatterns = [
    url(r'^login/$', login),
    url(r'^logout/$', logout),
    url(r'^account/$', account),
    url(r'^change_password/$', change_password),
]