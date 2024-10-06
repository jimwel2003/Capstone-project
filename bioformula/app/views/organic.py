from django.shortcuts import render, get_object_or_404
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
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max

def index(request):
    page = 'Organic'
    return render(request, 'app/organic.html', {'page': page})

def fertilizer(request):
    page = 'Organic'
    if request.method == "POST":
        try:
            form = FertilizerSearchForm(request.POST)
            if form.is_valid():
                search = form.cleaned_data['search']
                result = FertilizersIngredients.objects.filter(
                    Q(fertilizer__name__icontains=search) | Q(fertilizer__description__icontains=search) | Q(description__icontains=search)
                )
                paginator = Paginator(result, 20)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                form = FertilizerSearchForm()
                return render(request, 'app/fertilizer.html', {'page': page, 'form': form, 'list_': page_obj})
            else:
                messages.warning(request, form.errors)
        except Exception as e:
            messages.error(request, str(e))
    fertilizer = Fertilizers.objects.filter(status=True).annotate(max_rating=Max('fertilizerfeedback__rating')).order_by('-max_rating')
    paginator = Paginator(fertilizer, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    form = FertilizerSearchForm()
    return render(request, 'app/fertilizer.html', {'page': page, 'form': form, 'list': page_obj})

def fertilizer_details(request, id):
    page = 'Organic'
    instance = get_object_or_404(Fertilizers, pk=id)
    details = Fertilizers.objects.filter(fertilizer_id=id)
    ing = FertilizersIngredients.objects.filter(fertilizer_id=id)
    proc = FertilizersProcedure.objects.filter(fertilizer_id=id)
    feedback = FertilizerFeedback.objects.filter(fertilizer_id=id)
    source = FertilizerSource.objects.filter(fertilizer_id=id)
    for i in feedback:
        profile = Profile.objects.filter(user_id=i.user_id)
        for x in profile:
            if x.image:
                i.image = x.image
            else:
                i.image = settings.MEDIA_URL + "dp/default.jpeg"
    form = FertilizerConversionForm(instance=instance)
    return render(request, 'app/fertilizer-details.html', {'page': page, 'details': details, 'ing': ing, 'proc': proc, 'feedback': feedback, 'id': id, 'form': form, 'source': source })

def post_fertilizer_feedback(request, id):
    try:
        if request.method == "POST":
            feedbacks = request.POST.get('feedback')
            rating = request.POST.get('rating')
            with transaction.atomic():
                add_feedback = FertilizerFeedback(user_id=request.session['userid'], fertilizer_id=id, rating=rating, feedback=feedbacks, datetime_posted=timezone.now())
                add_feedback.save()
                if add_feedback.feedback_id:
                    messages.success(request, 'Your feedback is posted successfully')
            return HttpResponseRedirect("/fertilizer-details/" + str(id) + "#comment")
    except Exception as e:
        messages.error(request, str(e))
        return HttpResponseRedirect("/fertilizer-details/" + str(id) + "#comment")
    

def pesticide(request):
    page = 'Organic'
    if request.method == "POST":
        try:
            form = PesticideSearchForm(request.POST)
            if form.is_valid():
                search = form.cleaned_data['search']
                result = PesticideIngredients.objects.filter(
                    Q(pesticide__name__icontains=search) | Q(pesticide__description__icontains=search) | Q(description__icontains=search)
                )
                paginator = Paginator(result, 20)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                form = PesticideSearchForm()
                return render(request, 'app/pesticide.html', {'page': page, 'form': form, 'list_': page_obj})
            else:
                messages.warning(request, form.errors)
        except Exception as e:
            messages.error(request, str(e))
    pesticide = Pesticides.objects.filter(status=True).annotate(max_rating=Max('pesticidefeedback__rating')).order_by('-max_rating')
    paginator = Paginator(pesticide, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    form = PesticideSearchForm()
    return render(request, 'app/pesticide.html', {'page': page, 'form': form, 'list': page_obj})

def pesticide_details(request, id):
    page = 'Organic'
    instance = get_object_or_404(Pesticides, pk=id)
    details = Pesticides.objects.filter(pesticide_id=id)
    ing = PesticideIngredients.objects.filter(pesticide_id=id)
    proc = PesticideProcedure.objects.filter(pesticide_id=id)
    feedback = PesticideFeedback.objects.filter(pesticide_id=id)
    source = PesticideSource.objects.filter(pesticide_id=id)
    for i in feedback:
        profile = Profile.objects.filter(user_id=i.user_id)
        for x in profile:
            if x.image:
                i.image = x.image
            else:
                i.image = settings.MEDIA_URL + "dp/default.jpeg"
    form = PesticideConversionForm(instance=instance)
    return render(request, 'app/pesticide-details.html', {'page': page, 'details': details, 'ing': ing, 'proc': proc, 'feedback': feedback, 'id': id, 'form': form, 'source': source})


def post_pesticide_feedback(request, id):
    try:
        if request.method == "POST":
            feedbacks = request.POST.get('feedback')
            rating = request.POST.get('rating')
            with transaction.atomic():
                add_feedback = PesticideFeedback(user_id=request.session['userid'], pesticide_id=id, rating=rating, feedback=feedbacks, datetime_posted=timezone.now())
                add_feedback.save()
                if add_feedback.feedback_id:
                    messages.success(request, 'Your feedback is posted successfully')
            return HttpResponseRedirect("/pesticide-details/" + str(id) + "#comment")
    except Exception as e:
        messages.error(request, str(e))
        return HttpResponseRedirect("/pesticide-details/" + str(id) + "#comment")

@csrf_exempt
def pesticide_conversion(request):
    if request.method == 'POST':
        try:
            uom_qty = request.POST.get('uom_qty') or 0
            uom = request.POST.get('uom')
            land_qty = request.POST.get('land_qty') or 0
            land = request.POST.get('land')
            define = request.POST.get('define')
            id = request.POST.get("id")
            db_uom_qty = 0
            db_land_qty = 0
            data = PesticideConversion.objects.filter(pesticide_id=id, uom_id=uom, land_id=land)
            if data:
                for i in data:
                    db_uom_qty = i.uom_qty
                    db_land_qty = i.land_qty
                if define == 'UOM':
                    result = (float(uom_qty) * float(db_land_qty))/float(db_uom_qty)
                if define == "LAND":
                    result = (float(db_uom_qty) * float(land_qty))/float(db_land_qty)
                response = {
                    'status': 'success',
                    'result':  result,
                }
            else:
                response = {
                    'status': 'success',
                    'result':  0,
                }
        except:
            response = {
                'status': 'error',
            }
        return JsonResponse(response)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def fertilizer_conversion(request):
    if request.method == 'POST':
        try:
            uom_qty = request.POST.get('uom_qty') or 0
            uom = request.POST.get('uom')
            land_qty = request.POST.get('land_qty') or 0
            land = request.POST.get('land')
            define = request.POST.get('define')
            id = request.POST.get("id")
            db_uom_qty = 0
            db_land_qty = 0
            data = FertilizerConversion.objects.filter(fertilizer_id=id, uom_id=uom, land_id=land)
            if data:
                for i in data:
                    db_uom_qty = i.uom_qty
                    db_land_qty = i.land_qty
                if define == 'UOM':
                    result = (float(uom_qty) * float(db_land_qty))/float(db_uom_qty)
                if define == "LAND":
                    result = (float(db_uom_qty) * float(land_qty))/float(db_land_qty)
                response = {
                    'status': 'success',
                    'result':  result,
                }
            else:
                response = {
                    'status': 'success',
                    'result':  0,
                }
        except Exception as e:
            response = {
                'status': 'error',
            }
        return JsonResponse(response)
    return JsonResponse({'error': 'Invalid request'}, status=400)