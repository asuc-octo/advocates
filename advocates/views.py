from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from django.shortcuts import render_to_response, render, redirect, get_object_or_404
from django.utils import timezone
from .forms import UserForm
from django.contrib.auth.models import User

def index(request):
    return render_to_response('general/index.html')

def create(request): 
	if request.method == 'POST':
		form = UserForm(request.POST)
		if form.is_valid(): 
			print form.cleaned_data
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			email = form.cleaned_data.get('email')
			first_name = form.cleaned_data.get('first_name')
			last_name = form.cleaned_data.get('last_name')
			user = User.objects.create_user(username, email, password)
			user.first_name = first_name
			user.last_name = last_name
			user.save()
			return redirect('login')

	else: 
		form = UserForm()
	return render(request, 'new_user.html', {'form': form})
