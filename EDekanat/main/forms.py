from django import forms
from .models import Group, Document

class StudentSearchForm(forms.Form):
    zalikbook = forms.CharField(label="Номер залікової книжки")
    last_name = forms.CharField(label="Прізвище")
    first_name = forms.CharField(label="Ім’я")
    middle_name = forms.CharField(label="По-батькові")

    group = forms.ModelChoiceField(
        label='Група',
        queryset=Group.objects.all(),
        empty_label='Оберіть групу',
    )

    requesteddocument = forms.ModelChoiceField(
        label='Бажаний документ',
        queryset=Document.objects.all(),
        empty_label='Оберіть документ',
    )
    # course = forms.ModelChoiceField(
    #     label='Курс',
    #     queryset=Course.objects.all(),
    #     empty_label='Оберіть курс',
    # )
    # email = forms.EmailField(required=False) — лише для повідомлень

