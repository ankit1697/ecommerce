from django import forms
from django.forms import ModelForm

from products.models import *

class DateForm(ModelForm):
	class Meta:
		model = Order
		fields = ('delivery', 'delivery_time', 'comments', )
		widgets = {
			'delivery': forms.DateInput(attrs={'class': 'datepicker font-small', 'required': 'required'}),
			'delivery_time': forms.DateInput(attrs={'class': 'timepicker font-small', 'required': 'required'}),
			'comments': forms.TextInput(attrs={'class': 'form-control font-small'}),
		}

	def clean_delivery(self):
		delivery_date = self.cleaned_data['delivery']
		if delivery_date < datetime.datetime.now().date():
			raise ValidationError('Please select a date after today')
		return delivery_date