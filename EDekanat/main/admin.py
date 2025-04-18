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
from reportlab.lib.utils import ImageReader


from django.core.mail import EmailMessage
# Register your models here.

from django.contrib import messages

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

        student = Student.objects.filter(zalikbook=request_obj.student.zalikbook).first()

        # Реєстрація шрифту для підтримки кирилиці
        font_path = finders.find('fonts/timesnrcyrmt.ttf')
        pdfmetrics.registerFont(TTFont('TimesNewRoman', font_path))
        p.setFont('TimesNewRoman', 12)

        # Шапка документу
        p.drawCentredString(300, 765, "МІНІСТЕРСТВО ОСВІТИ І НАУКИ УКРАЇНИ")
        p.drawCentredString(300, 750, "КИЇВСЬКИЙ НАЦІОНАЛЬНИЙ УНІВЕРСИТЕТ імені Тараса Шевченка")
        p.drawCentredString(300, 735, "ФАКУЛЬТЕТ ІНФОРМАЦІЙНИХ ТЕХНОЛОГІЙ")
        p.drawCentredString(300, 720, "Кафедра програмних систем і технологій")

        # Контактна інформація (менший шрифт)
        p.setFont('TimesNewRoman', 10)
        contact_line1 = "вул. Богдана Гаврилишина, 24, м. Київ, 01042, тел./факс +38 044 529 1423"
        contact_line2 = "Email: fitdekanat@knu.ua, код ЄДРПОУ 00301931"
        p.drawCentredString(300, 705, contact_line1)
        p.drawCentredString(300, 695, contact_line2)

        # Номер довідки та дата
        p.setFont('TimesNewRoman', 12)
        p.drawString(75, 675, "_____ № _____")

        # Заголовок
        p.drawCentredString(300, 655, "ДОВІДКА")

        # Основний текст довідки
        text_y = 635
        p.setFont('TimesNewRoman', 12)

        student_name = f"{student.lastname} {student.firstname} {student.middlename}"
        course = get_object_or_404(Course, pk=student.courseid_id)
        speciality = get_object_or_404(Speciality, pk=student.specialityid_id)

        text_lines = [
            f"Видана здобувачу {student_name.upper()} в тому, що він дійсно є здобувачем",
            f"{course.number} курсу ОС 'бакалавр' денної форми навчання спеціальності",
            f"'{speciality.name}' за освітньою програмою '{speciality.description}'",
            f"факультету інформаційних технологій Київського національного університету",
            f"імені Тараса Шевченка 4 рівня акредитації.",
            "",
            "Зарахований наказом ректора 'Про зарахування за державним замовленням'",
            "№3208-33 від 10.08.25 року",
            "",
            "Початок навчання 01 вересня 2025 року.",
            "",
            "Закінчує навчання 30 червня 2029 року.",
            "",
            "Видана для подання за місцем вимоги."
        ]

        for line in text_lines:
            p.drawString(75, text_y, line)
            text_y -= 20
        

        # Підписи
        text_y -= 40

        dekanat_worker = get_object_or_404(DekanatWorkers, pk=request_obj.given_by_id)
        p.drawString(450, text_y - 20, f"{dekanat_worker.firstname} {dekanat_worker.lastname.upper()}")

        p.drawString(75, text_y, "Відповідальний працівник")
        p.drawString(75, text_y - 20, "деканату з навчально-виховної роботи")

        stamp_path = finders.find('img/stamp.png')  

        if stamp_path:
            stamp = ImageReader(stamp_path)
            p.drawImage(stamp, 320, 260, width=125, height=100, 
                    preserveAspectRatio=True, mask='auto')

        # Завершення сторінки
        p.showPage()
        p.save()
                
        buffer.seek(0)
        return buffer

    def generate_pdf_view(self, request, request_id):
        request_obj = get_object_or_404(Requests, pk=request_id)

        if request_obj.given_by is None:
            self.message_user(request, "Не обрано відповідального працівника деканату.", level=messages.ERROR)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        # Використовуємо загальний метод для генерації PDF
        buffer = self.generate_pdf_buffer(request_obj)

        # Повертаємо PDF у відповіді
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="request_{request_obj.id}.pdf"'
        return response

    def send_pdf_by_email(self, request, request_id):
        request_obj = get_object_or_404(Requests, pk=request_id)

        if request_obj.given_by is None:
            self.message_user(request, "Не обрано відповідального працівника деканату.", level=messages.ERROR)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

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

