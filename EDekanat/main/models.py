from django.db import models

# Create your models here.
class Speciality(models.Model):
    name = models.CharField(max=50, unique=True)
    description = models.CharField(max=100)

    class Meta:
        ordering=['name']

    def __str__(self):
        return self.name