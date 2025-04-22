from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator

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
    number = models.IntegerField()
    specialityid = models.ForeignKey(Speciality, on_delete=models.CASCADE)

    class Meta:
        ordering = ['number']
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
        constraints = [
            models.UniqueConstraint(fields=['number', 'specialityid'], name='unique_course_speciality')
        ]

    def __str__(self):
        return f"{self.number} курс ({self.specialityid.name})"


class Group(models.Model):
    name = models.CharField(max_length=50, unique=True)
    courseid =models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
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
    name = models.CharField(max_length=50, unique=True)
    documenttypeid = models.ForeignKey(Documenttype, on_delete=models.CASCADE)

    class Meta:
        ordering=['name']
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'

    def __str__(self):
        return self.name

class Student(models.Model):
    zalikbook = models.IntegerField(
            primary_key=True,
            validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)]
        )
    firstname = models.CharField(max_length=20, unique=False)
    middlename = models.CharField(max_length=20, unique=False)
    lastname = models.CharField(max_length=20, unique=False)
    groupid = models.ForeignKey(Group, on_delete=models.CASCADE)
    courseid = models.ForeignKey(Course, on_delete=models.CASCADE)
    specialityid = models.ForeignKey(Speciality, on_delete=models.CASCADE)
    email = models.EmailField(max_length=30, unique=True)
   
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

    contractnumber = models.CharField(max_length=8, unique=True)

    class Meta:
        ordering = ['zalikbook']
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self):
        return f"{self.firstname} {self.lastname} ({self.zalikbook})"

class Requests(models.Model):
    student = models.ForeignKey('Student', on_delete=models.PROTECT, related_name='requests')
    requested_document = models.ForeignKey('Document', on_delete=models.PROTECT,related_name='requests')
    status = models.BooleanField(default=False)  
    created_at = models.DateTimeField(auto_now_add=True)  
    given_by = models.ForeignKey('DekanatWorkers', on_delete=models.SET_NULL, null=True, blank=True, related_name='handled_requests')  # хто видав документ
    comment = models.CharField(max_length=255, blank=True) 

    class Meta:
        verbose_name = "Request"
        verbose_name_plural = "Requests"
        ordering = ['-created_at'] 
    def __str__(self):
        return f"Request by {self.student} for {self.requested_document} (Status: {'Done' if self.status else 'Pending'})"
