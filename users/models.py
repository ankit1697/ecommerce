from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class CustomUser(AbstractUser):
	phone = models.CharField('Phone Number', max_length=10, blank=False)
	email = models.EmailField(_('email address'), unique=True)

	# def get_address(self):
	# 	return customer.customeraddress_set.filter(selected=True)

ORDER_STATUS = (
	("Home", "Home"),
	("Work", "Work"),
	("Other", "Other"),
)


class CustomerAddress(models.Model):
	customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	area = models.CharField('Area', max_length=100)
	house_no = models.CharField('House/Flat #', max_length=100)
	landmark = models.CharField('Landmark', max_length=100)
	pincode = models.CharField('Pincode', max_length=6)
	category = models.CharField(max_length=20, choices=ORDER_STATUS, default='Home')
	category_string = models.CharField('Alias', max_length=20, default='Alias')
	selected = models.BooleanField(default=False)


	def get_phone(self):
		return self.customer.phone

	def full_address(self):
		return self.house_no + ' , ' + self.area + ' , ' + self.landmark + ' , ' + self.pincode