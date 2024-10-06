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
from django.db.models import Q

def index(request):
    page = 'Reservation'
    if request.session['group'] == 'Admin':
        return HttpResponseRedirect("/admin-reservation")
    else:
        reservations = Appointments.objects.filter(user_id=request.session['userid'])
        paginator = Paginator(reservations, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'app/reservation.html', {'page': page, 'list': page_obj})

def admin_reservation(request):
    page = 'Reservation'
    reservations = Appointments.objects.all().order_by('-date_created')
    paginator = Paginator(reservations, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'app/reservation-admin.html', {'page': page, 'list': page_obj})

def reservation_details(request, id):
    page = 'Reservation'
    if request.session['group']:
        if request.method == 'POST':
            try:
                form = ReservationDetailsForm(request.POST)
                if form.is_valid():
                    with transaction.atomic():
                        # event_type = form.cleaned_data['event_type']
                        start = form.cleaned_data['start']
                        # end = form.cleaned_data['end']
                        # days = form.cleaned_data['days']
                        notes = form.cleaned_data['notes']
                        status = form.cleaned_data['status']
                        reservation = Appointments.objects.get(appointment_id=id)
                        reservation.notes = notes
                        reservation.status = status
                        reservation.start = start
                        reservation.save()
                        messages.success(request, 'Reservation updated')
                else:
                    messages.warning(request, form.errors)
            except Exception as e:
                messages.error(request, str(e))
            return HttpResponseRedirect("/reservation-details/" + id)
        try:
            reservation = Appointments.objects.filter(appointment_id=id)
            for i in reservation:
                initial_value = {
                    'event_type'        : i.event_type,
                    'start'             : i.start,
                    'end'               : i.end,
                    'duration'          : i.duration,
                    'notes'             : i.notes,
                    'status'            : i.status,
                }
        except:
            initial_value = []
        form = ReservationDetailsForm(initial=initial_value)
        getDisableDates = Appointments.objects.all()
        disabledDates = []
        for i in getDisableDates:
            disabledDates.append(datetime.strftime(i.start, "%Y-%m-%d"))
        return render(request, 'app/reservation-details.html', {'page': page, 'form': form, 'id': id, 'disabledDates': disabledDates})
    else:
        return HttpResponseRedirect("/reservation#reservation")

def add(request):
    page = 'Reservation'
    if request.method == "POST":
        try:
            form = ReservationForm(request.POST)
            if form.is_valid():
                event_type = form.cleaned_data['event_type']
                start = form.cleaned_data['start']
                end = form.cleaned_data['end']
                duration = form.cleaned_data['duration']
                with transaction.atomic():
                    reserve = Appointments(user_id=request.session['userid'], event_type=event_type, start=start, end=end, duration=duration, date_created=timezone.now())
                    reserve.save()
                    if reserve.appointment_id:
                        messages.success(request, "Reservation Created, We will send you an email with regards to the status of your reservation")
                        return HttpResponseRedirect("/new-reservation#reservation")
            else:
                messages.warning(request, form.errors)
        except Exception as e:
            messages.error(request, str(e))
    form = ReservationForm()
    getDisableDates = Appointments.objects.all()
    disabledDates = []
    for i in getDisableDates:
        disabledDates.append(datetime.strftime(i.start, "%Y-%m-%d"))
    return render(request, 'app/new_reservation.html', {'page': page, 'form': form, 'disabledDates': disabledDates})
