from django.contrib import admin
from .models import Speciality, Course, Documenttype, Document
# Register your models here.

@admin.register(Speciality)
class SpecialityAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    list_filter = ['name']
    
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['number', 'specialityid']
    list_filter = ['number']

@admin.register(Documenttype)
class DocumenttypeAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['name', 'documenttypeid']
    list_filter = ['name']