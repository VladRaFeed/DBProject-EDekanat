from django.shortcuts import render
from .forms import StudentSearchForm
from .models import Student, Group, Requests

def students_form(request):
    form = StudentSearchForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        zalikbook = form.cleaned_data['zalikbook']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        middle_name = form.cleaned_data['middle_name']
        group_name = form.cleaned_data['group']

        group = form.cleaned_data['group']
        if not group:
            form.add_error('group', 'Групу не знайдено.')
        else:

            student = Student.objects.filter(
                zalikbook=zalikbook,
                firstname__iexact=first_name,
                lastname__iexact=last_name,
                middlename=middle_name,
                groupid=group
            ).first()

            if student:
                requested_document = form.cleaned_data['requesteddocument']
                Requests.objects.create(
                    student=student,
                    requested_document=requested_document
                )
                return render(request, 'main/form-completed.html', {
                    # 'form': form,
                    'student': student
                })

    return render(request, 'main/home-form.html', {'form': form})
