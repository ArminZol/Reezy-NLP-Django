from django.conf.urls import url

from .views import (
	home,
	simp_page,
	survey,
)

urlpatterns = [
    url(r'^$', home),
    url(r'^simp/$', simp_page),
    url(r'^survey/$', survey),
]