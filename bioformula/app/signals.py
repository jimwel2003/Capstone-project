from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *
from django.db import transaction
from .email import *

@receiver(post_save, sender=Appointments)
def appointment_emails(sender, instance, **kwargs):
    event_type = instance.event_type
    start = instance.start
    end = instance.end
    duration = instance.duration
    notes = instance.notes
    status = instance.status
    user_id = instance.user_id
    #to be define
    contact_email = "biofarmula3@gmail.com"
    contact_phone = "(054) 881-1033"
    farm_name = "BioFarmula"
    website_url = "www.Biofarmula.com"
    user = User.objects.filter(id=user_id)
    try:
        for i in user:
            customer_name = i.first_name + " " + i.last_name
            customer_email = i.email
    except:
        customer_name = ""
        customer_email
        pass

    if status == 'RESERVED':
        send_reservation_confirmation(customer_name, customer_email, event_type, start, end, duration, notes, contact_email, contact_phone, farm_name, website_url)
    elif status == 'RE-SCHEDULE':
        send_reservation_reschedule(customer_name, customer_email, event_type, start, end, duration, notes, contact_email, contact_phone, farm_name, website_url)
    elif status == 'CANCEL':
        send_reservation_cancelled(customer_name, customer_email, event_type, start, end, duration, notes, contact_email, contact_phone, farm_name, website_url)
    elif status == 'PENDING':
        send_reservation_pending(customer_name, customer_email, event_type, start, end, duration, notes, contact_email, contact_phone, farm_name, website_url)