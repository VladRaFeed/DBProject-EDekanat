from django.shortcuts import render

namespace = 'main'
# Create your views here.
def students_form(request):
    return render(request, 'main/home-form.html')