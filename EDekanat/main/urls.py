from django.urls import path, include
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.students_form, name='students_form'),
    # path('requests/<int:request_id>/pdf/', views.generate_pdf_view, name='generate-request-pdf'),
]

