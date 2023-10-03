from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf.urls import handler400, handler403, handler404, handler500

from rest_framework import routers

from users.views import *
from products.views import *

handler404 = 'products.views.page_not_found_view'
# handler500 = 'users.views.my_custom_error_view'
# handler403 = 'website.views.my_custom_permission_denied_view'
# handler400 = 'website.views.my_custom_bad_request_view'

router = routers.DefaultRouter()
router.register(r'api/categories', CategoryViewSet)
router.register(r'api/items', ItemViewSet)
router.register(r'api/users', UserViewSet)
router.register(r'api/addresses', UserAddressViewSet)
# router.register(r'api/carts', CartViewSet)
# router.register(r'api/cart_items', CartItemViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ItemListView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    # path('register/', RegisterView.as_view(), name='register'),
    url(r"^accounts/", include("django.contrib.auth.urls")),
    path('accounts/', include('allauth.urls')),
    path('accounts/<int:address_pk>/<int:user_pk>/delete_address', delete_address, name='delete_address'),
    path('accounts/<int:address_pk>/<int:user_pk>/update_address', update_address, name='update_address'),
    path('accounts/<int:address_pk>/<int:user_pk>/primary_address', primary_address, name='primary_address'),

    path('<int:pk>/<int:cat_pk>', item_description, name='itemdescription'),
    path('category/<int:pk>/', category_items, name='category_items'),
    path('<int:pk>/update', update_view, name='updatedetails'),
    path('accounts/<int:pk>/', user_details, name='userdetails'),

    path('cart/add_index/<int:pk>/<int:cat_pk>', cart_add_index, name='cart_add_index'),
    path('cart/item_clear/<int:pk>/<int:user_pk>', item_clear, name='item_clear'),
    path('cart/item_increment/<int:pk>/<int:user_pk>', item_increment, name='item_increment'),
    path('cart/item_decrement/<int:pk>/<int:user_pk>', item_decrement, name='item_decrement'),
    path('cart/cart_clear/<int:user_pk>', cart_clear, name='cart_clear'),
    path('cart/cart-detail/<int:pk>',cart_detail,name='cart_detail'),

    path('order-summary/<int:pk>/', order_summary, name='order_summary'),
    path('accounts/<int:pk>/order_history', order_history, name='order_history'),
    path('accounts/<int:pk>/address_list', address_list, name='address_list'),
    path('order_cancel/<int:order_pk>/<int:user_pk>', order_cancel, name='order_cancel'),
    path('reorder/<int:order_pk>/<int:user_pk>', reorder, name='reorder'),
    url(r'^search/', searchproducts, name='searchproducts'),

    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('verification/', include('verify_email.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)