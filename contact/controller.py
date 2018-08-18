from django.core.mail import send_mail

from datetime import datetime

from pytz import timezone

def complete_contact(request, form):
	fmt = '%Y-%m-%d %H:%M:%S %Z%z'

	eastern = timezone('US/Eastern')

	naive_dt = datetime.now()

	loc_dt = datetime.now(eastern)

	subject = "Support Ticket: " + loc_dt.strftime(fmt)

	text = form.cleaned_data.get('content') + "\n\n" + form.cleaned_data.get('name') + "\n" + form.cleaned_data.get('email')

	if request.user.is_authenticated():
		text = form.cleaned_data.get('content') + "\n\n" + request.user.first_name + ' ' + request.user.last_name + "\n" + request.user.email

	send_mail(subject, text, 'no-reply@reezyapp.com', ['support@reezyapp.com'])