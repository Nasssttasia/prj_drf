from django.core.mail import send_mail

from config import settings
from course.models import Course


def send_mail_delay(id_course):
    course = Course.objects.filter(pk=id_course).first()
    if course:
        subscriptions = course.subscription_set.all()
        emails = [x.user.email for x in subscriptions]
        print(emails)
        send_mail(
            subject='Обновление курса',
            message=f'Здравствуйте! Курс {course.title} обновился. Скорее посмотрите изменения!',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=emails
        )



