from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import *

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'


class PesticideIngredientsStacked(admin.StackedInline):
    model = PesticideIngredients
    initial_num = 1
    list_display = ("description")

    def get_extra(self, request, obj=None, **kwargs):
        if obj is not None:
            try:
                return max(self.initial_num - obj.answers.count(), 1)
            except:
                pass
        return self.initial_num
    
class PesticideProcedureStacked(admin.StackedInline):
    model = PesticideProcedure
    initial_num = 1
    list_display = ("procedure")

    def get_extra(self, request, obj=None, **kwargs):
        if obj is not None:
            try:
                return max(self.initial_num - obj.answers.count(), 1)
            except:
                pass
        return self.initial_num
    
class PesticideConversionStacked(admin.StackedInline):
    model = PesticideConversion
    initial_num = 1
    list_display = ("pesticide", "uom_qty", "uom", "land_qty", "land", "status")

    def get_extra(self, request, obj=None, **kwargs):
        if obj is not None:
            try:
                return max(self.initial_num - obj.answers.count(), 1)
            except:
                pass
        return self.initial_num

class PesticideSourceStacked(admin.StackedInline):
    model = PesticideSource
    initial_num = 1
    list_display = ("pesticide", "source", "link", "status")

    def get_extra(self, request, obj=None, **kwargs):
        if obj is not None:
            try:
                return max(self.initial_num - obj.answers.count(), 1)
            except:
                pass
        return self.initial_num
    
class FertilizerIngredientsStacked(admin.StackedInline):
    model = FertilizersIngredients
    initial_num = 1
    list_display = ("description")

    def get_extra(self, request, obj=None, **kwargs):
        if obj is not None:
            try:
                return max(self.initial_num - obj.answers.count(), 1)
            except:
                pass
        return self.initial_num
    
class FertilizerProcedureStacked(admin.StackedInline):
    model = FertilizersProcedure
    initial_num = 1
    list_display = ("procedure")

    def get_extra(self, request, obj=None, **kwargs):
        if obj is not None:
            try:
                return max(self.initial_num - obj.answers.count(), 1)
            except:
                pass
        return self.initial_num
    
class FertilizerConversionStacked(admin.StackedInline):
    model = FertilizerConversion
    initial_num = 1
    list_display = ("fertilizer", "uom_qty", "uom", "land_qty", "land", "status")

    def get_extra(self, request, obj=None, **kwargs):
        if obj is not None:
            try:
                return max(self.initial_num - obj.answers.count(), 1)
            except:
                pass
        return self.initial_num

class FertilizerSourceStacked(admin.StackedInline):
    model = FertilizerSource
    initial_num = 1
    list_display = ("fertilizer", "source", "link", "status")

    def get_extra(self, request, obj=None, **kwargs):
        if obj is not None:
            try:
                return max(self.initial_num - obj.answers.count(), 1)
            except:
                pass
        return self.initial_num

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Pesticides)
class PesticideAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "status")
    search_fields = ['name', 'description']
    inlines = [
        PesticideIngredientsStacked,
        PesticideProcedureStacked,
        PesticideConversionStacked,
        PesticideSourceStacked,
    ]

@admin.register(Fertilizers)
class FertilizerAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "status")
    search_fields = ['name', 'description']
    inlines = [
        FertilizerIngredientsStacked,
        FertilizerProcedureStacked,
        FertilizerConversionStacked,
        FertilizerSourceStacked,
    ]

@admin.register(Appointments)
class AppointmentsAdmin(admin.ModelAdmin):
    list_display = ("event_type", "start", "end", "duration")

admin.site.register(UOM)
admin.site.register(LandMeasure)
