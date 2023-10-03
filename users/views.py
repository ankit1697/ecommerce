from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, HttpResponseRedirect

from users.models import *

from users.forms import *

from verify_email.email_handler import send_verification_email

class LoginView(auth_views.LoginView):
	form_class = LoginForm
	template_name = 'registration/login.html'


class RegisterView(generic.CreateView):
	form_class = RegisterForm
	template_name = 'registration/register.html'
	success_url = reverse_lazy('login')


def user_details(request, pk):
	user = CustomUser.objects.get(id=pk)

	form = UserUpdateForm(request.POST or None, instance=user)
	if form.is_valid(): 
		form.save() 
		return redirect('/accounts/'+str(pk))

	return render(request, 'user_details.html', {'user': user, 'form': form})


def update_view(request, pk): 
	context ={}
	obj = get_object_or_404(CustomUser, id=pk) 
	form = UserUpdateForm(request.POST or None, instance=obj)
	if form.is_valid(): 
		form.save() 
		return redirect('/accounts/'+str(pk))
  
	context["form"] = form
  
	return render(request, "update_user_details.html", context)


def delete_address(request, address_pk, user_pk):
	user = get_object_or_404(CustomUser, id=user_pk) 
	CustomerAddress.objects.filter(id=address_pk).delete()

	if len(CustomerAddress.objects.filter(customer=user_pk)) != 0:
		last_address = CustomerAddress.objects.filter(customer=user).last()
		last_address.selected = True
		last_address.save()

	return redirect('/accounts/'+str(user_pk) + '/address_list')


def update_address(request, address_pk, user_pk): 
	context ={}
	user = get_object_or_404(CustomUser, id=user_pk)
	address = CustomerAddress.objects.get(id=address_pk)
	form = AddressUpdateForm(request.POST or None, instance=address)
	if form.is_valid(): 
		form.save() 
		return redirect('/accounts/'+str(user_pk)+'/address_list')
  
	context["form"] = form
  
	return render(request, "update_address.html", context)


def primary_address(request, address_pk, user_pk):
	CustomerAddress.objects.filter(customer=user_pk).update(selected=False)
	CustomerAddress.objects.filter(id=address_pk, customer=user_pk).update(selected=True)

	return redirect('/accounts/'+str(user_pk) + '/address_list')