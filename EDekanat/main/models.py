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