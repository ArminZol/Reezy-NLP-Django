from django.shortcuts import render
from django.http import HttpResponse

from controller import predict

def word_classifier(request):
	return HttpResponse('Feature currently not available')

	if 'word' in request.GET:
		return HttpResponse(predict(request.GET['word']))