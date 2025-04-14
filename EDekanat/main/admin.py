from django.contrib import admin
from .models import Group, DekanatWorkers, Speciality

# Register your models here.

@admin.register(Speciality)
class SpecialityAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    list_filter = ['name']

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'courseid']
    list_filter = ['courseid']

@admin.register(DekanatWorkers)
class DekanatWorkersAdmin(admin.ModelAdmin):
    list_display = ['firstname', 'middlename', 'lastname']  
    list_filter = ['lastname']  