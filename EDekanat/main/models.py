from django.db import models

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
        return str(self.number)
    
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