from django.contrib import admin
from .models import Speciality, Course, Documenttype, Document, Group, DekanatWorkers, Student, Requests
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.staticfiles import finders

import io
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import fonts
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics


from django.core.mail import EmailMessage
# Register your models here.

@admin.register(Speciality)
class SpecialityAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    list_filter = ['name']
    
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['number', 'specialityid']
    list_filter = ['number']

@admin.register(Documenttype)
class DocumenttypeAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['name', 'documenttypeid']
    list_filter = ['name']

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'courseid']
    list_filter = ['courseid']

@admin.register(DekanatWorkers)
class DekanatWorkersAdmin(admin.ModelAdmin):
    list_display = ['firstname', 'middlename', 'lastname', 'phonenumber', 'email']  
    list_filter = ['lastname']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = [
        'zalikbook',
        'firstname',
        'middlename',
        'lastname',
        'groupid',
        'courseid',
        'specialityid',
        'email',
        'phonenumber',
        'contractnumber',
    ]
    list_filter = ['lastname', 'groupid', 'courseid', 'specialityid']

@admin.register(Requests)
class RequestsAdmin(admin.ModelAdmin):
    change_form_template = "admin/request_change_form.html"

    list_display = [
        'student',
        'requested_document',
        'status',
        'created_at',
        'given_by',
        'comment',
    ]
    list_filter = ['status', 'created_at', 'given_by']
    search_fields = ['student__zalikbook', 'student__firstname', 'student__lastname']

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:request_id>/pdf/', 
                self.admin_site.admin_view(self.generate_pdf_view), 
                name='generate-request-pdf',
            ),
            path(
                '<int:request_id>/send-pdf-by-mail/', 
                self.admin_site.admin_view(self.send_pdf_by_email), 
                name='send-pdf-by-mail',
            ),
        ]
        return custom_urls + urls

    def generate_pdf_buffer(self, request_obj):
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)

        # Зареєструємо шрифт
        font_path = finders.find('fonts/timesnrcyrmt.ttf')
        pdfmetrics.registerFont(TTFont('TimesNewRoman', font_path))

        # Встановлюємо шрифт для кирилиці
        p.setFont('TimesNewRoman', 12)

        # Генеруємо вміст для PDF (заповнюємо даними з request_obj)
        p.drawString(100, 780, f"Запит №: {request_obj.id}")
        p.drawString(100, 760, f"Студент: {request_obj.student}")
        p.drawString(100, 740, f"Документ: {request_obj.requested_document}")
        p.drawString(100, 720, f"Статус: {request_obj.status}")

        # Завершуємо створення сторінки
        p.showPage()
        p.save()

        # Повертаємо PDF у пам'яті
        buffer.seek(0)
        return buffer

    def generate_pdf_view(self, request, request_id):
        # Отримуємо об'єкт запиту
        request_obj = get_object_or_404(Requests, pk=request_id)

        # Використовуємо загальний метод для генерації PDF
        buffer = self.generate_pdf_buffer(request_obj)

        # Повертаємо PDF у відповіді
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="request_{request_obj.id}.pdf"'
        return response

    def send_pdf_by_email(self, request, request_id):
        # Отримуємо об'єкт запиту
        request_obj = get_object_or_404(Requests, pk=request_id)

        # Використовуємо загальний метод для генерації PDF
        buffer = self.generate_pdf_buffer(request_obj)

        # Отримуємо email адреса для відправки
        student = Student.objects.filter(zalikbook=request_obj.student.zalikbook).first()
        recipient_email = student.email  # Наприклад, одержувач

        # Створюємо email
        email = EmailMessage(
            subject=f"Запит № {request_obj.id} - PDF документ",
            body=f"Шановний {student.firstname} {student.lastname}, додано PDF документ для запиту № {request_obj.id}.",
            from_email="loram.hoptan@gmail.com",  # Ваша email адреса
            to=[recipient_email]
        )

        # Додаємо PDF як вкладення
        email.attach(f"request_{request_obj.id}.pdf", buffer.read(), "application/pdf")

        # Відправляємо email
        email.send()

        # Повідомлення для адміна
        self.message_user(request, "PDF документ надіслано на пошту.")

        # Перенаправлення на попередню сторінку
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

