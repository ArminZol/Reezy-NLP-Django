from django.conf.urls import url

from .views import (
	quest,
)

urlpatterns = [
    url(r'^', quest),
]