from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms

from users.models import *


class RegisterForm(UserCreationForm):
	class Meta:
		model = get_user_model()
		# fields = ('email', 'username', 'password1', 'password2', 'phone', 'address',)
		fields = ('email', 'username', 'password1', 'password2', 'phone')


class LoginForm(AuthenticationForm):
	email = forms.EmailField(label='Email')


class UserUpdateForm(forms.ModelForm):
	class Meta: 
		model = get_user_model()
		# fields = ('email', 'username', 'phone', 'address')
		fields = ('first_name', 'last_name', 'phone')
		widgets = {
			'first_name': forms.TextInput(attrs={'class': 'form-control'}),
			'last_name': forms.TextInput(attrs={'class': 'form-control'}),
			'phone': forms.TextInput(attrs={'class': 'form-control', 'pattern': '[0-9]{10}', 'required':'required'}),
		}


class AddressAddForm(forms.ModelForm):
	# specify the name of model to use
	class Meta:
		model = CustomerAddress
		exclude = ['selected', 'customer']
		widgets = {
			'area': forms.TextInput(attrs={'class': 'form-control'}),
			'house_no': forms.TextInput(attrs={'class': 'form-control'}),
			'landmark': forms.TextInput(attrs={'class': 'form-control'}),
			'pincode': forms.TextInput(attrs={'class': 'form-control', 'minlength':6}),
			'category': forms.Select(attrs={'class': 'form-control'}),
			'category_string': forms.TextInput(attrs={'class': 'form-control', 'id':'alias_field'}),
		}

	def clean_pincode(self):
		pincode = self.cleaned_data['pincode']
		if not (pincode.isdigit() and len(pincode) == 6):    
			raise ValidationError('Invalid pincode format', params={'pincode': pincode},)
		return pincode


class AddressUpdateForm(forms.ModelForm):
	class Meta: 
		model = CustomerAddress
		# fields = ('email', 'username', 'phone', 'address')
		fields = ('house_no', 'area', 'landmark', 'pincode', 'category', 'category_string')
		widgets = {
			'area': forms.TextInput(attrs={'class': 'form-control'}),
			'house_no': forms.TextInput(attrs={'class': 'form-control'}),
			'landmark': forms.TextInput(attrs={'class': 'form-control'}),
			'pincode': forms.TextInput(attrs={'class': 'form-control'}),
			'category': forms.Select(attrs={'class': 'form-control'}),
			'category_string': forms.TextInput(attrs={'class': 'form-control', 'id':'alias_field'}),
		}