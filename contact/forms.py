from django import forms

class ContactForm(forms.Form):
	name = forms.CharField(max_length=20, required=False, widget=forms.TextInput())
	email = forms.EmailField(required=True, widget=forms.EmailInput())
	content = forms.CharField(required=True, widget=forms.Textarea(attrs={'class' : "materialize-textarea"}))