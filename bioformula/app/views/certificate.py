from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User, Group
from datetime import date, datetime, timedelta, timezone
from django.db import transaction
from django.contrib.sessions.models import Session
from django.core.paginator import Paginator
from ..forms import *
from ..models import *
from ..email import *
from django.db.models import Q

def index(request):
    page = 'Certificate'
    try:
        if request.session['group'] != 'Admin':
            return HttpResponseRedirect("/")
        if request.method == "POST":
                form = CertificateForm(request.POST)
                if form.is_valid():
                    name = form.cleaned_data['name']
                    email = form.cleaned_data['email']
                    inclusive_date = form.cleaned_data['inclusive_date']
                    details = form.cleaned_data['details']
                    signatory = form.cleaned_data['signatory']
                    send_certificate(name, email, inclusive_date, details, signatory)
                    messages.success(request, 'Certificate Sent')
                    return HttpResponseRedirect("/certificate")
                else:
                    messages.warning(request, form.errors)
        form = CertificateForm()
        return render(request, 'app/certificate.html', {'page': page, 'form': form})
    except Exception as e:
        messages.error(request, str(e))
        return HttpResponseRedirect("/certificate")

