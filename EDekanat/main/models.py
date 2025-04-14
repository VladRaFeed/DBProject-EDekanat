from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=50, unique=True)
    courseid = models.IntegerField()

    class Meta:
        db_table = 'groups'
        ordering=['name']
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'
    

    def __str__(self):
        return self.name
    
class DekanatWorkers(models.Model):
    firstname = models.CharField(max_length=50)
    middlename = models.CharField(max_length=50, blank=True, null=True)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, unique=True)
    phonenumber_regex = RegexValidator(
        regex=r'^\+380\d{9}$',
        message="Номер телефону повинен бути у форматі: '+380XXXXXXXXX'.",
    )
    phonenumber = models.CharField(
        validators=[phonenumber_regex],
        max_length=13,
        unique=True,
    )

    class Meta: 
        db_table = 'dekanatworkers'

    def __str__(self):
        return f"{self.firstname} {self.middlename} {self.lastname}" if self.middlename else f"{self.firstname} {self.lastname}"
    
    class Speciality(models.Model):
        name = models.CharField(max_length=50, unique=True)
        description = models.CharField(max_length=100)


    class Meta:
        ordering=['name']
        verbose_name = 'Speciality'
        verbose_name_plural = 'Specialities'

    def __str__(self):
        return self.name