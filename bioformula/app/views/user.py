from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User, Group
from datetime import date, datetime, timedelta
from django.db import transaction
from django.contrib.auth import authenticate, login
from django.contrib.sessions.models import Session
from ..forms import *
from ..email import *

def validation(request, id):
    if request.method == "POST":
        try:
            form = ValidationForm(request.POST)
            if form.is_valid():
                with transaction.atomic():
                    firstname = form.cleaned_data['firstname'].upper()
                    middlename = form.cleaned_data['middlename'].upper() if form.cleaned_data['middlename'] is not None else ''
                    lastname = form.cleaned_data['lastname'].upper()
                    email = form.cleaned_data['email']
                    suffix = form.cleaned_data['suffix'].upper() if form.cleaned_data['suffix'] is not None else ''
                    civil_status = form.cleaned_data['civil_status']
                    gender = form.cleaned_data['gender']
                    occupation = form.cleaned_data['occupation'].upper()
                    address = form.cleaned_data['address'].upper()
                    contact_no = form.cleaned_data['contact_no']
                    password = form.cleaned_data['password']
                    user = User.objects.get(id=id)
                    user.first_name = firstname
                    user.last_name = lastname
                    user.email = email
                    user.username = email
                    user.set_password(password)
                    user.save()
                    profile = Profile.objects.get(user_id=id)
                    profile.middlename = middlename
                    profile.suffix = suffix
                    profile.civil_status = civil_status
                    profile.gender = gender
                    profile.occupation = occupation
                    profile.address = address
                    profile.phone = contact_no
                    profile.save()
                    user = authenticate(request, username=email, password=password)
                    if user is not None:
                        login(request, user)
                        request.session['first_name'] = user.first_name
                        request.session['last_name'] = user.last_name
                        request.session['email'] = user.username
                        request.session['userid'] = user.id
                        group = user.groups.all()
                        for i in group:
                            request.session['group'] = i.name
                        return HttpResponseRedirect('/')
            else:
                messages.warning(request, form.errors)
        except Exception as e:
            messages.error(request, str(e))
    try:
        profile = Profile.objects.filter(user_id=id)
        for i in profile:
            initial_value = {
                'firstname'         : i.user.first_name,
                'middlename'        : i.middlename,
                'lastname'          : i.user.last_name,
                'email'             : i.user.email,
                'suffix'            : i.suffix,
                'civil_status'      : i.civil_status,
                'gender'            : i.gender,
                'occupation'        : i.occupation,
                'address'           : i.address,
                'contact_no'        : i.phone
            }
    except:
        initial_value = []
        pass
    form = ValidationForm(initial=initial_value)
    return render(request, 'app/validation.html', {'form': form, 'id': id})

def profile(request, id):
    page = 'Profile'
    if request.method == "POST":
        try:
            form = ProfileForm(request.POST, request.FILES)
            if form.is_valid():
                with transaction.atomic():
                    firstname = form.cleaned_data['firstname'].upper()
                    middlename = form.cleaned_data['middlename'].upper() if form.cleaned_data['middlename'] is not None else ''
                    lastname = form.cleaned_data['lastname'].upper()
                    email = form.cleaned_data['email']
                    suffix = form.cleaned_data['suffix'].upper() if form.cleaned_data['suffix'] is not None else ''
                    civil_status = form.cleaned_data['civil_status']
                    gender = form.cleaned_data['gender']
                    occupation = form.cleaned_data['occupation'].upper()
                    address = form.cleaned_data['address'].upper()
                    contact_no = form.cleaned_data['contact_no']
                    image_file = form.cleaned_data['image']
                    user = User.objects.get(id=id)
                    user.first_name = firstname
                    user.last_name = lastname
                    user.email = email
                    user.username = email
                    user.save()
                    profile = Profile.objects.get(user_id=id)
                    profile.middlename = middlename
                    profile.suffix = suffix
                    profile.civil_status = civil_status
                    profile.gender = gender
                    profile.occupation = occupation
                    profile.address = address
                    profile.phone = contact_no
                    if image_file:
                        profile.image = image_file
                    profile.save()
                    messages.success(request, "Profile updated")
            else:
                messages.warning(request, form.errors)
        except Exception as e:
            messages.error(request, str(e))
    try:
        profile = Profile.objects.filter(user_id=id)
        for i in profile:
            initial_value = {
                'firstname'         : i.user.first_name,
                'middlename'        : i.middlename,
                'lastname'          : i.user.last_name,
                'email'             : i.user.email,
                'suffix'            : i.suffix,
                'civil_status'      : i.civil_status,
                'gender'            : i.gender,
                'occupation'        : i.occupation,
                'address'           : i.address,
                'contact_no'        : i.phone,
                'image'             : i.image,
            }
    except Exception as e:
        initial_value = []
        pass
    form = ProfileForm(initial=initial_value)
    return render(request, 'app/profile.html', {'form': form, 'id': id, 'page': page})

