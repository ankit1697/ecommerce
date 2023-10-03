from rest_framework import serializers
from django.contrib.auth import get_user_model

from products.models import *
from users.models import *

class CategorySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Category
		fields = ('id', 'name', 'main_category', 'image', )


class ItemSerializer(serializers.HyperlinkedModelSerializer):
	# ...
	category_id = serializers.IntegerField(write_only=True)
	category = CategorySerializer(read_only=True)
	# ...
	class Meta:
		model = Item
		fields = ('category_id', 'category', 'name', )


class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = get_user_model()
		fields = ('id', 'email', 'first_name', 'last_name', 'phone', )


class UserAddressSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = CustomerAddress
		fields = '__all__'