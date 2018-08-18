from processing import dictionary_api

from controller import convert_tags

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail

from datetime import datetime

from pytz import timezone

import requests

SIMPLIFIER_PAGE = '/simp/'
CONTACT_PAGE = '/contact/'
API_PAGE = '/quest/'
ACCOUNT_PAGE = '/users/account/'
LOGIN_PAGE = '/users/login/'
LOGOUT_PAGE = '/users/logout/'

def home(request):
	context = {}

	if request.user.is_authenticated():
		links = [SIMPLIFIER_PAGE, ACCOUNT_PAGE, LOGOUT_PAGE]
		titles = ['Simplifier', 'Account','Logout']
		context['zippped_list'] = zip(links, titles)
	else:
		links = [LOGIN_PAGE]
		titles = ['Login']
		context['zippped_list'] = zip(links, titles)

	return render(request, 'general/home.html', context)

def survey(request):
	if request.user.is_authenticated() and request.user.username == 'shoop':
		context = {}
		
		links = [SIMPLIFIER_PAGE, ACCOUNT_PAGE, LOGOUT_PAGE]
		titles = ['Simplifier', 'Account','Logout']
		context['zippped_list'] = zip(links, titles)

		return render(request, 'functions/word_survey.html', context)
	else:
		return HttpResponse("Oi!")

def simp_page(request):
	if request.user.is_authenticated():
		if request.method == 'POST':
			fmt = '%Y-%m-%d %H:%M:%S %Z%z'

			eastern = timezone('US/Eastern')

			naive_dt = datetime.now()

			loc_dt = datetime.now(eastern)

			subject = "Report: " + loc_dt.strftime(fmt)

			text = "Input: " + request.POST.get('text') #Text that gets submitted to slack
			result = 'Result: ' + convert_tags(request.POST.get('result'))
			stats = 'Stats: ' + convert_tags(request.POST.get('stats'))
			name = 'Name: ' + request.user.first_name + ' ' + request.user.last_name
			username = 'Username: ' + request.user.username
			user_email = 'Email: ' + request.user.email

			text += '\n' + result + '\n' + stats + '\n' + name + '\n' + username + '\n' + user_email


			send_mail(subject, text, 'no-reply@reezyapp.com', ['reports@reezyapp.com'])

		return render(request, 'functions/simplifier_page.html')
	else:
		return redirect(LOGIN_PAGE)