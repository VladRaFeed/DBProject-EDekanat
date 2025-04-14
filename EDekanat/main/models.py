from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
class Speciality(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=100)


    class Meta:
        ordering=['name']
        verbose_name = 'Speciality'
        verbose_name_plural = 'Specialities'

    def __str__(self):
        return self.name
    
class Course(models.Model):
    number = models.IntegerField(unique=False)
    specialityid = models.ForeignKey(Speciality, on_delete=models.CASCADE)


    class Meta:
        ordering=['number']
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'

    def __str__(self):
        return f"{self.number} курс ({self.specialityid.name})"

class Group(models.Model):
    name = models.CharField(max_length=50, unique=True)
    courseid =models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        ordering=['name']
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'
    

    def str(self):
        return self.name
    
class DekanatWorkers(models.Model):
    firstname = models.CharField(max_length=50)
    middlename = models.CharField(max_length=50, blank=True, null=True)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, unique=True)

    phone_regex = RegexValidator(
        regex=r'^\+380\d{9}$',
        message="Номер телефону повинен бути у форматі: '+380XXXXXXXXX'."
    )

    phonenumber = models.CharField(
        validators=[phone_regex],
        max_length=13,
        unique=True,
        verbose_name="Phone Number"
    )

    class Meta: 
        ordering = ['firstname']
        verbose_name = 'Dekanat Worker'
        verbose_name_plural = 'Dekanat Workers'

    def __str__(self):
        if self.middlename:
            return f"{self.firstname} {self.middlename} {self.lastname}"
        return f"{self.firstname} {self.lastname}"
    
class Documenttype(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering=['name']
        verbose_name = 'Document Type'
        verbose_name_plural = 'Document Types'

    def __str__(self):
        return self.name

class Document(models.Model):
    name = models.CharField(max_length=50, unique=False)
    documenttypeid = models.ForeignKey(Documenttype, on_delete=models.CASCADE)

    class Meta:
        ordering=['name']
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'

    def __str__(self):
        return self.name