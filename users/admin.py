from django.contrib import admin
from users.models import *

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', )

class AddressAdmin(admin.ModelAdmin):
	list_display = ('house_no', 'customer', 'get_phone', 'selected', )

admin.site.register(CustomUser, UserAdmin)
admin.site.register(CustomerAddress, AddressAdmin)