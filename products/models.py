from django.db import models
from users.models import *

import datetime

MAIN_CATEGORY = (
	("Sweet", "Sweet"),
	("Savoury", "Savoury"),
)

class Category(models.Model):
	name = models.CharField(max_length=100)
	main_category = models.CharField(max_length=20, choices=MAIN_CATEGORY, default='Sweet')
	image = models.ImageField(upload_to='logos', blank=True, null=True)

	def __str__(self):
		return self.name


class Banner(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	image = models.ImageField(upload_to='banner', blank=True, null=True)

	def __str__(self):
		return self.category.name


class Item(models.Model):
	name = models.CharField(max_length=300)
	slug = models.SlugField(max_length=150)
	description = models.TextField()
	image = models.ImageField(upload_to='product_photo', blank=True, null=True)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	price = models.DecimalField(max_digits=6, decimal_places=2)
	new = models.BooleanField(default=False)
	featured = models.BooleanField(default=False)
	order_count = models.IntegerField(default=0)

	def __str__(self):
		return self.name


class OrderItem(models.Model):
	item = models.ForeignKey(Item, on_delete=models.CASCADE)
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	ordered = models.BooleanField(default=False)
	quantity = models.IntegerField(default=1)

	def item_quantity(self):
		return self.item.name + '--' + str(self.quantity)



ORDER_STATUS = (
	("Pending", "Pending"),
	("Completed", "Completed"),
	("Cancelled", "Cancelled"),
)

class Order(models.Model):
	item = models.ManyToManyField(OrderItem)
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	address = models.ForeignKey(CustomerAddress, on_delete=models.CASCADE, null=True, blank=True)
	amount = models.DecimalField(max_digits=10, decimal_places=2)
	delivery = models.DateField('Delivery Date', default=datetime.datetime.now().date()+datetime.timedelta(1))
	delivery_time = models.TimeField(default='20:00')
	ordered_date = models.DateTimeField()
	completed = models.BooleanField(default=False)
	status = models.CharField(max_length=20, choices=ORDER_STATUS, default='Pending')
	cancelled_on = models.DateTimeField(default=datetime.datetime.now(), blank=True)
	comments = models.CharField('Cooking Instructions', default='', max_length=50, blank=True)

	def item_quantity(self):
		return "-----".join([p.item.name + '(' + str(p.quantity) + ')' for p in self.item.all()])
