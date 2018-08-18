from django.conf.urls import url

from .views import (
	word_classifier,
)

urlpatterns = [
    url(r'^word_classifier/$', word_classifier),
]