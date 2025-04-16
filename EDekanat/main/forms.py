from django import forms
from .models import Group, Document

class StudentSearchForm(forms.Form):
    zalikbook = forms.CharField(label="Залікова книжка", widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label="Ім'я", widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label="Прізвище", widget=forms.TextInput(attrs={'class': 'form-control'}))
    middle_name = forms.CharField(label="По батькові", widget=forms.TextInput(attrs={'class': 'form-control'}))
    group = forms.ModelChoiceField(label="Група", queryset=Group.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}))
    requesteddocument = forms.ModelChoiceField(label="Бажаний документ", queryset=Document.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}))
