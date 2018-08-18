from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout, update_session_auth_hash

from processing import classifier_manager

from processing import personaliser

def sign_up_account(username, email, password, first_name, last_name):
	if User.objects.filter(username=username).exists():
		return False

	User.objects.create_user(username, email=email, password=password, first_name=first_name, last_name=last_name)

	# classifier_manager.classifiers[username] = personaliser.Personaliser(username)
	# classifier_manager.save()

	return True

def login_account(request, username, password):
	user = authenticate(username=username, password=password)

	if user is not None:
		if user.is_active:
			login(request, user)

			if user.username == 'shoop':
				if user.username not in classifier_manager.classifiers:
					classifier_manager.classifiers[user.username] = personaliser.Personaliser(user.username)
					classifier_manager.save()

			return True

	return False

def logout_account(request):
	logout(request)

def update_clf_in_accounts():
	all_users = User.objects.all()

	for user in all_users:
		classifier_manager.classifiers[user.username] = personaliser.Personaliser(user.username)

	classifier_manager.save()

def update_acccount(old_username, new_username, new_email, new_first_name, new_last_name):
	user = User.objects.get(username=old_username)

	user.username = new_username
	user.email = new_email
	user.first_name = new_first_name
	user.last_name = new_last_name
	
	user.save()

def update_password(request, username, new_password):
	user = User.objects.get(username=username)

	user.set_password(new_password)

	user.save()

	update_session_auth_hash(request, user)
