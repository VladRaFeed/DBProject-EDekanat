from django.contrib import admin
from .models import Speciality
# Register your models here.

@admin.register(Speciality)
class SpecialityAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    list_filter = ['name']
    
