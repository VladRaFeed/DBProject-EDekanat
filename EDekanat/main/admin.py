from django.contrib import admin
from .models import Speciality, Course, Documenttype, Document, Group, DekanatWorkers, Student, Requests
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.staticfiles import finders
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.utils import ImageReader
from datetime import datetime

from django.core.mail import EmailMessage
# Register your models here.

from django.contrib import messages

from transliterate import translit

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

    def generate_pdf_buffer(self, request, request_obj):
        if request_obj.requested_document.name not in ['Витяг про місце навчання', 'Довідка 20', 'Сертифікат про знання англійської мови']:
            self.message_user(request, f"Помилка: Немає шаблону для документу типу '{request_obj.requested_document.name}'", level=messages.ERROR)
            return None

        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)

        student = Student.objects.filter(zalikbook=request_obj.student.zalikbook).first()

        # Реєстрація шрифту для підтримки кирилиці
        font_path = finders.find('fonts/timesnrcyrmt.ttf')
        pdfmetrics.registerFont(TTFont('TimesNewRoman', font_path))
        p.setFont('TimesNewRoman', 12)


        if request_obj.requested_document.name == 'Витяг про місце навчання':
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
            p.drawString(75, 675, f"_____ № {request_obj.id}_____")

            # Заголовок
            p.drawCentredString(300, 655, "ДОВІДКА")

            # Основний текст довідки
            text_y = 635
            p.setFont('TimesNewRoman', 12)

            student_name = f"{student.lastname} {student.firstname} {student.middlename}"
            course = get_object_or_404(Course, pk=student.courseid_id)
            speciality = get_object_or_404(Speciality, pk=student.specialityid_id)

            text_lines = [
                f"Видана здобувачу {student_name.upper()} в тому, що він дійсно є",
                f"здобувачем освіти {course.number} курсу ОС 'бакалавр' денної форми навчання спеціальності",
                f"'{speciality.name}' за освітньою програмою '{speciality.description}'",
                f"факультету інформаційних технологій Київського національного університету",
                f"імені Тараса Шевченка 4 рівня акредитації.",
                "",
                "Зарахований наказом ректора 'Про зарахування за державним замовленням'",
                "№3208-33 від 10.08.25 року",
                "",
                f"Початок навчання 01 вересня {2025 - int(course.number)} року.",
                "",
                f"Закінчує навчання 30 червня {2025 + 4- int(course.number)} року.",
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

        elif request_obj.requested_document.name == 'Довідка 20':
            p.drawCentredString(300, 780, "УКРАЇНА")
            p.drawCentredString(300, 765, "КИЇВСЬКИЙ НАЦІОНАЛЬНИЙ УНІВЕРСИТЕТ")
            p.drawCentredString(300, 750, "ІМЕНІ ТАРАСА ШЕВЧЕНКА")
            
            # Дата (поточний рік)
            current_date = datetime.now().strftime('"%d"_____%m____ %Y р.')
            p.drawString(100, 735, current_date)
            
            # Номер довідки
            p.drawString(100, 720, f"№ {request_obj.id}/2025/12")
            
            # Адреса
            p.drawString(100, 705, "01601, м. Київ")
            p.drawString(100, 690, "вул. Володимирська, 64/13")
            
            # Заголовок додатка
            p.drawCentredString(300, 660, "Додаток 20")
            p.drawCentredString(300, 645, "до Положення")
            
            # Основний текст
            student = request_obj.student
            student_name = f"{student.lastname} {student.firstname} {student.middlename}"
            course = get_object_or_404(Course, pk=student.courseid_id)
            speciality = get_object_or_404(Speciality, pk=student.specialityid_id)
            
            text_lines = [
                f"Видана призовникові {student_name.upper()}",
                f"про те, що він у {2025 - int(course.number)} році вступив до",
                "Київського національного університету імені Тараса Шевченка",
                "(повне найменування закладу освіти)",
                f"і зараз навчається на {course.number} курсі денного відділення за спеціальністю {speciality.description}.",
                "",
                f"Строк закінчення закладу освіти 30 червня {2025 + 4 - int(course.number)} р.",
                "",
                "Довідку видано для подання до військомату"
            ]
            
            text_y = 600
            for line in text_lines:
                p.drawString(100, text_y, line)
                text_y -= 20
            
            # Підписи
            text_y -= 40
            p.drawString(75, text_y, "Виконувач обов'язків начальника")
            p.drawString(75, text_y-15, "військово-мобілізаційного підрозділу (відділу)")
            
            dekanat_worker = get_object_or_404(DekanatWorkers, pk=request_obj.given_by_id)
            p.drawString(475, text_y - 15, f"{dekanat_worker.firstname} {dekanat_worker.lastname.upper()}")

            # Печатка (якщо потрібна)
            stamp_path = finders.find('img/stamp.png')  

            if stamp_path:
                stamp = ImageReader(stamp_path)
                p.drawImage(stamp, 350, 315, width=125, height=100, 
                        preserveAspectRatio=True, mask='auto')

        elif request_obj.requested_document.name == 'Сертифікат про знання англійської мови':
            knulogo_path = finders.find('img/knulogo.png')
            if knulogo_path:
                knulogo = ImageReader(knulogo_path)
                p.drawImage(knulogo, 260, 695, width=80, height=80, preserveAspectRatio=True, mask='auto')  # y +125

            # === HEADER ===
            p.setFont('TimesNewRoman', 14)
            p.drawCentredString(300, 675, "LANGUAGE PROFICIENCY ASSESSMENT FORM")  # y +125
            p.drawCentredString(300, 655, "FROM HOME UNIVERSITY")  # y +125

            # === BASIC INFO ===
            p.setFont('TimesNewRoman', 12)
            p.drawString(80, 635, "LANGUAGE TO BE ASSESSED: English")  # y +125

            # === APPLICANT INFORMATION BOX ===
            p.rect(80, 535, 440, 90)  # y +125
            p.drawString(90, 605, f"Name of Applicant: {translit(student.lastname, 'uk', reversed=True)} {translit(student.firstname, 'uk', reversed=True)} {translit(student.middlename, 'uk', reversed=True)}")  # y +125
            p.drawString(90, 585, "Level of the Applicant: Undergraduate")  # y +125
            p.drawString(90, 565, "Home University: Taras Shevchenko National University of Kyiv")  # y +125
            p.drawString(90, 545, "Country: Ukraine")  # y +125

            # === CERTIFICATION BOX ===
            p.rect(80, 385, 440, 140)  # y +125
            certification_text = [
                "This is to certify that the above named applicant has",
                "demonstrated English language proficiency at level:",
                "B1 (Intermediate) according to the Common European",
                "Framework of Reference for Languages (CEFR).",
                "",
                "The assessment was conducted according to the standards",
                "of the Language Center of Taras Shevchenko National",
                "University of Kyiv."
            ]
            text_y = 510  # 385 + 125
            for line in certification_text:
                p.drawString(90, text_y, line)
                text_y -= 15

            p.setFont('TimesNewRoman', 8)
            p.drawString(90, 395, "The University assumes full responsibility for the validity and accuracy of this assessment.")  # y +125

            # === SIGNATURE BOX ===
            p.rect(80, 205, 440, 160)  # y +125

            p.setFont('TimesNewRoman', 12)
            p.drawString(90, 345, "Certified by:")  # y +125
            p.drawString(90, 325, "Name: __Laura Liashenko________")  # y +125
            p.drawString(90, 305, "Position:")  # y +125

            # Two-column checkboxes
            left_column = [
                ("☐ Language Instructor", 90, 285),
                ("☐ International Office", 90, 265)
            ]
            right_column = [
                ("☐ Department Head", 270, 285),
                ("☐ Faculty Dean", 270, 265)
            ]
            for text, x, y in left_column + right_column:
                p.drawString(x, y, text)

            # "x" in checkbox manually positioned if needed
            p.drawString(92, 286, "x")  # y +125

            # SIGNATURE AND DATE
            p.drawString(90, 235, "Signature: _________________________")  # y +125
            p.drawString(400, 235, f"Date: {datetime.now().strftime('%d %B %Y')}")  # y +125

            # STAMP (right-aligned inside box)
            stamp_path = finders.find('img/stamp.png')
            if stamp_path:
                stamp = ImageReader(stamp_path)
                p.drawImage(stamp, 200, 190, width=100, height=100, preserveAspectRatio=True, mask='auto')  # y +125





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
        buffer = self.generate_pdf_buffer(request, request_obj)

        if buffer is None:  # Якщо шаблон не знайдено
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
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
        buffer = self.generate_pdf_buffer(request,request_obj)

        if buffer is None:  # Якщо шаблон не знайдено
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
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

