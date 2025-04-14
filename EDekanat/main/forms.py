from django import forms
from .models import Group, DekanatWorkers

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name','courseid',]

class DekanatWorkersForm(forms.ModelForm):
    class Meta:
        model = DekanatWorkers
        fields = '__all__'
