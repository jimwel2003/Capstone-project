from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User, Group
from datetime import date, datetime, timedelta
from django.db import transaction
from django.contrib.sessions.models import Session
from ..forms import *
from ..email import *

def index(request):
    form = RegisterForm()
    page = "Home"
    return render(request, 'app/index.html', {'form': form, 'page': page})

def register(request):
    if request.method == "POST":
        try:
            form = RegisterForm(request.POST)
            if form.is_valid():
                firstname = form.cleaned_data['firstname'].upper()
                middlename = form.cleaned_data['middlename'].upper() if form.cleaned_data['middlename'] is not None else ''
                lastname = form.cleaned_data['lastname'].upper()
                email = form.cleaned_data['email']
                with transaction.atomic():
                    user = User.objects.create_user(username=email, email=email, first_name=firstname, last_name=lastname, password="Zaq12wsx")
                    user.save()
                    if user.id:
                        profile = Profile(user_id=user.id, middlename=middlename)
                        profile.save()
                        if profile.user_id:
                            send_registration_success_email(firstname, email, profile.user_id)
                            return render(request, 'app/registration_success.html')
                        else:
                            messages.error(request, 'Opps! Error encountered, Please try again')
                    else:
                        messages.error(request, 'Opps! Error encountered, Please try again')
                    return HttpResponseRedirect("/#registration-form")
            else:
                messages.warning(request, form.errors)
        except Exception as e:
            messages.error(request, "The email address is already in use by another user.")
    else:
        messages.warning(request, "Invalid method used")
    return HttpResponseRedirect("/#registration-form")
