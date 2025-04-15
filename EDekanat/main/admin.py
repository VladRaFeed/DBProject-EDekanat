from django.contrib import admin
from .models import Speciality, Course, Documenttype, Document, Group, DekanatWorkers, Student
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

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'courseid']
    list_filter = ['courseid']

@admin.register(DekanatWorkers)
class DekanatWorkersAdmin(admin.ModelAdmin):
    list_display = ['firstname', 'middlename', 'lastname', 'phonenumber', 'email']  
    list_filter = ['lastname']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = [
        'zalikbook',
        'firstname',
        'middlename',
        'lastname',
        'groupid',
        'courseid',
        'specialityid',
        'email',
        'phonenumber',
        'contractnumber',
    ]
    list_filter = ['lastname', 'groupid', 'courseid', 'specialityid']