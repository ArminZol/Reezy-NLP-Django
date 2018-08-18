from django.shortcuts import render, redirect

from django.http import HttpResponse

from .forms import SignUpForm, LoginForm, AccountForm, PasswordChangeForm

from .controller import sign_up_account, login_account, logout_account, update_acccount, update_password

HOME_PAGE = '/'
SIMPLIFIER_PAGE = '/simp/'
ACCOUNT_CREATE_FAILED_PAGE = 'errors/account_create_failed.html'
ACCOUNT_PAGE = '/users/account/'
LOGIN_PAGE = '/users/login/'
LOGOUT_PAGE = '/users/logout/'
SIGN_UP_PAGE = '/users/sign_up/'

def sign_up(request):
	form = SignUpForm(request.POST or None)

	context = {
		'form': form
	}

	if form.is_valid():
		username = form.cleaned_data.get('username')
		email = form.cleaned_data.get('email')
		password = form.cleaned_data.get('password')
		first_name = form.cleaned_data.get('first_name')
		last_name = form.cleaned_data.get('last_name')

		if sign_up_account(username, email, password, first_name, last_name):
			if login_account(request, username, password):
				return redirect(SIMPLIFIER_PAGE)
		else:
			return render(request, ACCOUNT_CREATE_FAILED_PAGE)

	return render(request, 'users/sign_up.html', context)

def login(request):
	if request.user.is_authenticated():
		return redirect(SIMPLIFIER_PAGE)

	form = LoginForm(request.POST or None)

	context = {
		'form': form
	}

	if form.is_valid():
		username = form.cleaned_data.get('username')
		password = form.cleaned_data.get('password')

		if login_account(request, username, password):
			return redirect(SIMPLIFIER_PAGE)

	return render(request, 'users/login.html', context)

def logout(request):
	if request.user.is_authenticated():
		logout_account(request)
	
	return redirect(HOME_PAGE)

def account(request):
	if request.user.is_authenticated():
		initial = {
			'first_name': request.user.first_name, 
			'last_name': request.user.last_name, 
			'email': request.user.email, 
			'username': request.user.username
		}
		
		form = AccountForm(request.POST or None, user=request.user, initial=initial)

		context = {
			'form': form,
			'creation_date': request.user.date_joined,
			'last_login': request.user.last_login
		}

		if form.is_valid():
			update_acccount(request.user.username, form.cleaned_data.get('username'), form.cleaned_data.get('email'), form.cleaned_data.get('first_name'), form.cleaned_data.get('last_name'))

		return render(request, 'users/account.html', context)
	else:
		return redirect(SIGN_UP_PAGE)

def change_password(request):
	if request.user.is_authenticated():
		form = PasswordChangeForm(request.POST or None, user=request.user)

		context = {
			'form': form
		}

		if form.is_valid():
			update_password(request, request.user.username, form.cleaned_data.get('new_password'))
			return redirect(ACCOUNT_PAGE)

		return render(request, 'users/change_password.html', context)
	else:
		return redirect(SIGN_UP_PAGE)
