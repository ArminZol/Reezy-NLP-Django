from django.shortcuts import render

from django.http import HttpResponseRedirect

from .forms import ContactForm

from .controller import complete_contact

SIMPLIFIER_PAGE = '/simp/'
ACCOUNT_PAGE = '/users/account/'
LOGIN_PAGE = '/users/login/'
LOGOUT_PAGE = '/users/logout/'

def contact(request):
	form = ContactForm(request.POST or None)

	context = {}

	if request.user.is_authenticated():
		links = [SIMPLIFIER_PAGE, ACCOUNT_PAGE, LOGOUT_PAGE]
		titles = ['Simplifier', 'Account','Logout']
		context['zippped_list'] = zip(links, titles)

		initial = {
			'name': request.user.get_full_name(),
			'email': request.user.email,
		}

		form.initial = initial
	else:
		links = [LOGIN_PAGE]
		titles = ['Login']
		context['zippped_list'] = zip(links, titles)

	if request.method == 'POST' and form.is_valid():
		complete_contact(request, form)

		return HttpResponseRedirect("/")

		#form = ContactForm(request.POST or None)

	context['form'] = form

	return render(request, 'functions/contact_page.html', context)