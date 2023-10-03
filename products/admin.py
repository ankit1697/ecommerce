from django.contrib import admin
from products.models import *


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
	pass

class ItemAdmin(admin.ModelAdmin):
	list_display = ('name', 'category', 'price', 'order_count', 'featured',)

class OrderItemAdmin(admin.ModelAdmin):
	list_display = ('item_quantity', 'user', 'ordered')

class OrderAdmin(admin.ModelAdmin):
	list_display = ('ordered_date', 'user', 'address', 'delivery', 'delivery_time' ,'item_quantity', 'amount', 'status',)
	list_filter = ('status', )

class BannerAdmin(admin.ModelAdmin):
	pass

admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Banner, BannerAdmin)