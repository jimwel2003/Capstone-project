from typing import Any
from django.db import models
from django.db.models.fields import AutoField
from django.db.models.deletion import RESTRICT
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    middlename = models.CharField(max_length=150, null=True, blank=True)
    suffix= models.CharField(max_length=10, null=True, blank=True)
    civil_status = models.CharField(max_length=30, null=True, blank=True)
    gender = models.CharField(max_length=30, null=True, blank=True)
    occupation = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=250, null=True, blank=True)
    phone = models.CharField(max_length=30, null=True, blank=True)
    image = models.ImageField(upload_to='dp/', null=True, blank=True)

    def __str__(self):
        return self.user.username

class UOM(models.Model):
    uom_id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=50)
    abbr = models.CharField(max_length=10, null=True, blank=True)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Unit of Measurements'

    def __str__(self):
        return self.name
    
class LandMeasure(models.Model):
    land_id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=50)
    abbr = models.CharField(max_length=10, null=True, blank=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Pesticides(models.Model):
    pesticide_id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=500, null=True, blank=True)
    image = models.ImageField(upload_to='pesticide/', null=True, blank=True)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Pesticides"

class PesticideIngredients(models.Model):
    ingredient_id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    pesticide = models.ForeignKey(Pesticides, on_delete=RESTRICT)
    description = models.CharField(max_length=250)

    def __str__(self):
        return self.description

class PesticideProcedure(models.Model):
    procedure_id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    pesticide = models.ForeignKey(Pesticides, on_delete=RESTRICT)
    procedure = models.CharField(max_length=500)

class PesticideFeedback(models.Model):
    feedback_id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=RESTRICT)
    pesticide = models.ForeignKey(Pesticides, on_delete=RESTRICT)
    rating = models.IntegerField(default=0)
    feedback = models.CharField(max_length=250)
    datetime_posted = models.DateTimeField()

class PesticideConversion(models.Model):
    convert_id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    pesticide = models.ForeignKey(Pesticides, on_delete=RESTRICT)
    uom_qty = models.IntegerField(default=0)
    uom = models.ForeignKey(UOM, on_delete=RESTRICT)
    land_qty = models.IntegerField(default=0)
    land = models.ForeignKey(LandMeasure, on_delete=RESTRICT)
    status = models.BooleanField(default=True)

class PesticideSource(models.Model):
    source_id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    pesticide = models.ForeignKey(Pesticides, on_delete=RESTRICT)
    source = models.CharField(max_length=100, null=True, blank=True)
    link = models.CharField(max_length=250, null=True, blank=True)
    status = models.BooleanField(default=True)

class Fertilizers(models.Model):
    fertilizer_id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=500, null=True, blank=True)
    image = models.ImageField(upload_to='fertilizer/', null=True, blank=True)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Fertilizers"

class FertilizersIngredients(models.Model):
    ingredient_id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    fertilizer = models.ForeignKey(Fertilizers, on_delete=RESTRICT)
    description = models.CharField(max_length=250)

    def __str__(self):
        return self.description

class FertilizersProcedure(models.Model):
    procedure_id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    fertilizer = models.ForeignKey(Fertilizers, on_delete=RESTRICT)
    procedure = models.CharField(max_length=500)

class FertilizerFeedback(models.Model):
    feedback_id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=RESTRICT)
    fertilizer = models.ForeignKey(Fertilizers, on_delete=RESTRICT)
    rating = models.IntegerField(default=0)
    feedback = models.CharField(max_length=250)
    datetime_posted = models.DateTimeField()

class FertilizerConversion(models.Model):
    convert_id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    fertilizer = models.ForeignKey(Fertilizers, on_delete=RESTRICT)
    uom_qty = models.IntegerField(default=0)
    uom = models.ForeignKey(UOM, on_delete=RESTRICT)
    land_qty = models.IntegerField(default=0)
    land = models.ForeignKey(LandMeasure, on_delete=RESTRICT)
    status = models.BooleanField(default=True)

class FertilizerSource(models.Model):
    source_id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    fertilizer = models.ForeignKey(Fertilizers, on_delete=RESTRICT)
    source = models.CharField(max_length=100, null=True, blank=True)
    link = models.CharField(max_length=250, null=True, blank=True)
    status = models.BooleanField(default=True)

class Appointments(models.Model):
    appointment_id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=RESTRICT)
    approver = models.ForeignKey(User, on_delete=RESTRICT, null=True, blank=True, related_name='approver_%(class)s')
    event_type = models.CharField(max_length=150)
    start = models.DateField()
    end = models.DateField()
    duration = models.CharField(max_length=50, null=True, blank=True)
    notes = models.CharField(max_length=250)
    status = models.CharField(max_length=50, default='PENDING')
    date_created = models.DateTimeField()
    date_modified = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Appointments"

    def __str__(self):
        return self.event_type

class Notification(models.Model):
    notification_id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=RESTRICT)
    subject = models.CharField(max_length=100)
    body = models.CharField(max_length=500)
    sent_datetime = models.DateTimeField(null=True, blank=True)
    date_created = models.DateTimeField()
