from django.core.management import BaseCommand
from datetime import datetime
from course.models import Course, Lesson, Payments



class Command(BaseCommand):


    def handle(self, *args, **options):

        payments = [
            {'date_of_payment': '09.10.2023', 'paid_course': 'Курс 1', 'paid_lesson': None, 'payment_amount': '50000', 'payment_method': 'Наличные'},
            {'date_of_payment': '10.11.2023', 'paid_course': None, 'paid_lesson': 'Урок 1', 'payment_amount': '10000', 'payment_method': 'Перевод на счет'},
            ]

        payment_to_create = []

        # Перебираем платежи для изменения
        for payment in payments:

            # Приводим дату к виду YYYY-MM-DD
            payment['date_of_payment'] = datetime.strptime(payment['date_of_payment'], '%d.%m.%Y').strftime('%Y-%m-%d')


            # Получаем курс
            course_title = payment.get('paid_course')
            course = Course.objects.get(title=course_title)
            # Изменяем купленный курс на значение из базы данных
            payment = payment['paid_course'] = course

            # Получаем урок
            lesson_title = payment.get('paid_lesson')
            lesson = Lesson.objects.get(title=lesson_title)
            # Изменяем купленный урок на значение из базы данных
            payment = payment['paid_lesson'] = lesson


            # Добавляем продукты в новый список
            payment_to_create.append(
                Payments(**payment)
            )
