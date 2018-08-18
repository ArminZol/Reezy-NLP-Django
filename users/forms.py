from django import forms

from django.contrib.auth import authenticate

from django.contrib.auth.models import User

from django.utils.translation import ugettext as _

SCHOOL_MAX_LENGTH = 20
USERNAME_MAX_LENGTH = 20
FIRST_NAME_MAX_LENGTH = 20
LAST_NAME_MAX_LENGTH = 20
PASSWORD_MAX_LENGTH = 20
PASSWORD_MIN_LENGTH = 5

PASSWORD_TOO_SHORT_ERROR = 'Password must be at least {} chacacters long'.format(PASSWORD_MIN_LENGTH)

class SignUpForm(forms.Form):
	first_name = forms.CharField(max_length=FIRST_NAME_MAX_LENGTH, required=False, widget=forms.TextInput(attrs={'id' : "first_name", 'type' : "text"}))
	last_name = forms.CharField(max_length=LAST_NAME_MAX_LENGTH, required=False, widget=forms.TextInput(attrs={'id' : "last_name", 'type' : "text"}))
	email = forms.EmailField(widget=forms.TextInput(attrs={'id' : "email", 'type' : "email"}))
	username = forms.CharField(max_length=USERNAME_MAX_LENGTH, widget=forms.TextInput(attrs={'id' : "username", 'type' : "text"}))
	password = forms.CharField(max_length=PASSWORD_MAX_LENGTH, widget=forms.TextInput(attrs={'id' : "password", 'type' : "password"}))

	def clean_username(self):
		username = self.cleaned_data.get('username')

		if User.objects.filter(username=username).exists():
			raise forms.ValidationError(_("Username is already taken"), code='username taken')

		return username

	def clean_password(self):
		password = self.cleaned_data.get('password')

		if len(password) < PASSWORD_MIN_LENGTH:
			raise forms.ValidationError(_(PASSWORD_TOO_SHORT_ERROR), code='password too short')

		return password

class LoginForm(forms.Form):
	username = forms.CharField(max_length=USERNAME_MAX_LENGTH)
	password = forms.CharField(max_length=PASSWORD_MAX_LENGTH, widget=forms.PasswordInput())
	school = forms.CharField(max_length=SCHOOL_MAX_LENGTH)

	def clean(self):
		clean_username = self.cleaned_data.get('username')
		clean_password = self.cleaned_data.get('password')
		clean_school = self.cleaned_data.get('school').lower()

		if clean_username and clean_password:
			user = authenticate(username=clean_username, password=clean_password)
			if user is None:
				raise forms.ValidationError(_("Username or password is incorrect. Note that both fields are case-sensitive."), code='invalid')
			elif not user.groups.filter(name=clean_school).exists():
				raise forms.ValidationError(_("User does not exist within this school"), code='invalid')
			# elif not self.user_cache.is_active:
			# 	raise forms.ValidationError(_("This account is inactive."), code='inactive')

		return self.cleaned_data

class AccountForm(forms.Form):
	first_name = forms.CharField(widget=forms.TextInput(attrs={'disabled': 'true', 'id' : "first_name", 'type' : "text"}))
	last_name = forms.CharField(widget=forms.TextInput(attrs={'disabled': 'true', 'id' : "last_name", 'type' : "text"}))
	username = forms.CharField(widget=forms.TextInput(attrs={'disabled': 'true', 'id' : "username", 'type' : "text"}))
	email = forms.EmailField(widget=forms.EmailInput(attrs={'disabled': 'true', 'id' : "email", 'type' : "email"}))

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', None)
		super(AccountForm, self).__init__(*args, **kwargs)

	def clean_username(self):
		username = self.cleaned_data.get('username')
		
		if self.user.username != username and User.objects.filter(username=username).exists():
			raise forms.ValidationError(_("Username is already in use"), code='username taken')

		return username

class PasswordChangeForm(forms.Form):
	old_password = forms.CharField(max_length=PASSWORD_MAX_LENGTH, widget=forms.PasswordInput())
	new_password = forms.CharField(max_length=PASSWORD_MAX_LENGTH, widget=forms.PasswordInput())
	verify_new_password = forms.CharField(max_length=PASSWORD_MAX_LENGTH, widget=forms.PasswordInput())

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', None)
		super(PasswordChangeForm, self).__init__(*args, **kwargs)

	def clean_old_password(self):
		old_password = self.cleaned_data.get('old_password')

		if not self.user.check_password(old_password):
			raise forms.ValidationError(_("Incorrect password"), code='incorrect password')

		return old_password

	def clean_new_password(self):
		new_password = self.cleaned_data.get('new_password')

		if len(new_password) < PASSWORD_MIN_LENGTH:
			raise forms.ValidationError(_(PASSWORD_TOO_SHORT_ERROR), code='new password is too short')

		return new_password

	def clean_verify_new_password(self):
		verify_new_password = self.cleaned_data.get('verify_new_password')
		new_password = self.cleaned_data.get('new_password')

		if verify_new_password != new_password:
			raise forms.ValidationError(_("Passwords don't match"), code='passwords don\'t match')

		return verify_new_password