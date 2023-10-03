from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, HttpResponseRedirect
from django.db.models import Q
from django.template.loader import get_template
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets
from rest_framework import generics
from rest_framework.decorators import action

from .serializers import *
from products.forms import *
from users.models import *
from products.models import *
from cart.cart import Cart
from users.forms import *

import razorpay
import datetime


# Create your views here.
class ItemListView(generic.ListView):
	model = Item
	context_object_name = 'items'
	queryset = Item.objects.all()
	template_name = 'index.html'

	def get_context_data(self, **kwargs):
		context = super(ItemListView, self).get_context_data(**kwargs)
		context['category_list'] = Category.objects.all()
		context['banner_list'] = Banner.objects.all()
		context['featured_items'] = Item.objects.filter(featured=True)
		context['top_selling_items'] = Item.objects.all().order_by('-order_count')[:5]

		return context


def item_description(request, pk, cat_pk):
	item = Item.objects.get(id=pk)
	queryset = Item.objects.filter(category=cat_pk).exclude(id=pk)

	return render(request, 'item_description.html', {'item': item, 'item_list': queryset})


def category_items(request, pk):
	category = get_object_or_404(Category, id=pk)
	items = Item.objects.filter(category=category)
	return render(request, 'category_items.html', {'items': items})


def order_history(request, pk):
	user = get_object_or_404(CustomUser, id=pk)
	orders = Order.objects.filter(user=user).order_by('-pk')

	form = UserUpdateForm(request.POST or None, instance=user)
	if form.is_valid(): 
		form.save() 
		return redirect('/accounts/'+str(pk)+'/order_history')

	return render(request, 'order_history.html', {'orders': orders, 'form': form})


def address_list(request, pk):
	user = get_object_or_404(CustomUser, id=pk)
	address = CustomerAddress.objects.filter(customer=user)

	add_address_form = AddressAddForm(request.POST or None)
	  
	if add_address_form.is_valid():
		form_detail = add_address_form.save(commit=False)
		form_detail.customer = user

		CustomerAddress.objects.filter(customer=pk).update(selected=False)

		form_detail.selected = True

		form_detail.save()
		return redirect('/accounts/'+str(pk) + '/address_list')

	return render(request, 'address_list.html', {'addresses': address, 'address_add_form':add_address_form})



@login_required(login_url="/accounts/login")
def cart_add_index(request, pk, cat_pk):
	cart = Cart(request)
	product = Item.objects.get(id=pk)
	cart.add(product=product)
	return redirect(request.META['HTTP_REFERER'])


@login_required(login_url="/accounts/login")
def item_clear(request, pk, user_pk):
	cart = Cart(request)
	product = Item.objects.get(id=pk)
	cart.remove(product)
	return redirect("/cart/cart-detail/" + str(user_pk))


@login_required(login_url="/accounts/login")
def item_increment(request, pk, user_pk):
	cart = Cart(request)
	product = Item.objects.get(id=pk)
	cart.add(product=product)
	return redirect("/cart/cart-detail/" + str(user_pk))


@login_required(login_url="/accounts/login")
def item_decrement(request, pk, user_pk):
	cart = Cart(request)
	product = Item.objects.get(id=pk)
	cart.decrement(product=product)
	return redirect("/cart/cart-detail/" + str(user_pk))


@login_required(login_url="/accounts/login")
def cart_clear(request, pk):
	cart = Cart(request)
	cart.clear()
	return redirect("/cart/cart-detail/" + str(pk))


@login_required(login_url="/accounts/login")
def cart_detail(request, pk):
	context = {}
	total = 0
	items = []
	for key, value in request.session['cart'].items():
		total = total + float(value['quantity']) * float(value['price'])

	cart = Cart(request)
	if len(cart.cart) != 0:
		client = razorpay.Client(auth=('rzp_test_D0JJ4GnSjofFmJ', '0FYJC5yAlV6FgelcSASEJPcc'))
		response = client.order.create({'amount':total*100,'currency':'INR','payment_capture':1})
		context['response'] = response

	form = DateForm(request.POST or None)

	if request.method == 'POST':
		if form.is_valid():

			user = get_object_or_404(CustomUser, id=pk)
			address = CustomerAddress.objects.filter(customer=pk, selected=True)

			for key, value in request.session['cart'].items():
				product = Item.objects.get(id=value['product_id'])
				product.order_count = product.order_count + 1
				product.save()
				order_item = OrderItem.objects.create(user=user, item=product, quantity=value['quantity'], ordered=True)
				items.append(order_item)
			
			

			form_detail = form.save(commit=False)
			form_detail.user = user
			form_detail.ordered_date = datetime.datetime.now()
			form_detail.delivery = request.POST['delivery']
			form_detail.delivery_time = request.POST['delivery_time']
			form_detail.amount = total
			form_detail.address = address[0]
			form_detail.comments = request.POST['comments']

			form_detail.save()

			form_detail.item.add(*items)

			cart = Cart(request)
			cart.clear()

			send_order_place_email(user.id, user.first_name, user.email)

			return redirect('/order-summary/' + str(form_detail.pk))

	context['total'] = total
	context['form'] = form

	return render(request, 'cart/cart_detail.html', context)


def order_summary(request, pk):
	order = Order.objects.filter(id=pk)

	return render(request, "cart/order_details.html", {'order': order})


@login_required(login_url="/accounts/login")
def order_place(request, user_pk):
	total = 0
	items = []
	for key, value in request.session['cart'].items():
		total = total + float(value['quantity']) * float(value['price'])
	user = get_object_or_404(CustomUser, id=user_pk)
	for key, value in request.session['cart'].items():
		product = Item.objects.get(id=value['product_id'])
		order_item = OrderItem.objects.create(user=user, item=product, quantity=value['quantity'], ordered=True)
		items.append(order_item)

	address = CustomerAddress.objects.filter(customer=user_pk, selected=True)

	order = Order.objects.create(user=user, ordered_date=datetime.datetime.now().date(), delivery=request.session.get('delivery'), delivery_time=request.session.get('delivery_time'), amount=total, address=address[0])
	order.item.add(*items)

	# cart = Cart(request)
	# cart.clear()

	return render(request, "cart/order_details.html", {'order': order_item})

def order_cancel(request, order_pk, user_pk):
	user = get_object_or_404(CustomUser, id=user_pk)
	Order.objects.filter(id=order_pk).update(status='Cancelled', cancelled_on=datetime.datetime.now())

	send_order_cancel_email(user_pk, user.first_name, user.email)

	return redirect('/accounts/' + str(user_pk) + '/order_history')


def reorder(request, order_pk, user_pk):
	cart = Cart(request)
	order = Order.objects.get(id=order_pk)
	for item in order.item.all():
		product = Item.objects.get(id=item.item.id)
		cart.add(product=product)

	return redirect("/cart/cart-detail/" + str(user_pk))


def searchproducts(request):
	if request.method == 'GET':
		query= request.GET.get('q')
		print(query)

		submitbutton = request.GET.get('submit')

		if query is not None:
			lookups = Q(name__icontains=query) | Q(description__icontains=query) | Q(category__name__icontains=query)

			results = Item.objects.filter(lookups).distinct()

			context={'results': results,
					 'submitbutton': submitbutton}

			return render(request, 'search.html', context)

		else:
			return render(request, 'search.html')

	else:
		return render(request, 'search.html')



def send_order_place_email(user_id, first_name, to_email):
	#get template
	subject, from_email, to = 'Your Essencious order', settings.EMAIL_HOST_USER, to_email
	#pass the context to html template
	
	htmly = render_to_string("email_templates/order_confirmation.html", {"first_name": first_name, 'id': user_id})
	# html_content = htmly.render(d)
	msg = EmailMultiAlternatives(subject, htmly, from_email, [to])
	msg.attach_alternative(htmly, "text/html")
	msg.send()


def send_order_cancel_email(user_id, first_name, to_email):
	#get template
	subject, from_email, to = 'Your Essencious order', settings.EMAIL_HOST_USER, to_email
	#pass the context to html template
	
	htmly = render_to_string("email_templates/order_cancel.html", {"first_name": first_name, 'id': user_id})
	# html_content = htmly.render(d)
	msg = EmailMultiAlternatives(subject, htmly, from_email, [to])
	msg.attach_alternative(htmly, "text/html")
	msg.send()


def page_not_found_view(request, exception):
	response = render_to_response('404.html',context_instance=RequestContext(request))

	response.status_code = 404

	return response

class CategoryViewSet(viewsets.ModelViewSet):
	queryset = Category.objects.all()
	serializer_class = CategorySerializer


class ItemViewSet(viewsets.ModelViewSet):
	queryset = Item.objects.all()
	serializer_class = ItemSerializer


class UserViewSet(viewsets.ModelViewSet):
	queryset = CustomUser.objects.all()
	serializer_class = UserSerializer


class UserAddressViewSet(viewsets.ModelViewSet):
	queryset = CustomerAddress.objects.all()
	serializer_class = UserAddressSerializer