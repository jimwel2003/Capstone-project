from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User, Group
from datetime import date, datetime, timedelta
from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from ..forms import *
from ..email import *
import logging # used for logging system warning, error and critical bugs
logger = logging.getLogger(__name__) # global declaration for logger


def signin(request):
    if request.method == 'POST':
        username = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['first_name'] = user.first_name
                request.session['last_name'] = user.last_name
                request.session['email'] = user.username
                request.session['userid'] = user.id
                group = user.groups.all()
                if group:
                    for i in group:
                        request.session['group'] = i.name
                else:
                    request.session['group'] = ''
                return HttpResponseRedirect('/')
            
            else:
                messages.warning(request, 'Incorrect email or password')
        except Exception as e:
            messages.error(request, 'An error occured while signing in, Please try again')
            logger.error(str(e))
    form = SigninForm()
    page = 'Login'
    return render(request, 'app/signin.html', {'form': form, 'page': page})

def signout(request):
    logout(request)
    request.session.flush()
    return HttpResponseRedirect("/")

def forgot(request):
    if request.method == "POST":
        #to be define
        contact_email = "biofarmula3@gmail.com"
        contact_phone = "(054) 881-1033"
        farm_name = "BioFarmula"
        website_url = "www.Biofarmula.com"
        firstname = ""
        id = ""
        try:
            form = ForgotPasswordForm(request.POST)
            if form.is_valid():
                
                email = form.cleaned_data['email']
                if User.objects.filter(username=email).exists():
                    user = User.objects.filter(username=email)
                    for i in user:
                        firstname = i.first_name
                        id = i.id
                    send_password_reset(contact_email, email, farm_name, website_url, firstname, contact_phone, id)
                    messages.success(request, "Password reset instructions is sent to your email")
                else:
                    messages.warning(request, "Email Address does not exist")
                return HttpResponseRedirect("/forgot-password#forgot")
            else:
                messages.warning(request, form.errors)
        except Exception as e:
            messages.error(request, str(e))
    form = ForgotPasswordForm()
    page = 'Login'
    return render(request, 'app/forgot.html', {'form': form, 'page': page, 'form': form})

def new_password(request, id):
    try:
        if request.method == "POST":
            form = NewPasswordForm(request.POST)
            if form.is_valid():
                password = form.cleaned_data['password']
                with transaction.atomic():
                    user = get_object_or_404(User, id=id)
                    user.set_password(password)
                    user.save()
                    messages.success(request, 'Password changed, Please sign in')
                    return HttpResponseRedirect("/signin#login")
            else:
                messages.warning(request, form.errors)
        form = NewPasswordForm()
        page = 'Login'
        return render(request, 'app/new-password.html', {'form': form, 'page': page, 'form': form, 'id': id})
    except Exception as e:
        print(str(e))
        messages.error(request, 'Invalid request sent')
        return HttpResponseRedirect("/new-password/id#forgot")