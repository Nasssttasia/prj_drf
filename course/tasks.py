from celery import shared_task

from course.services import send_mail_delay


@shared_task
def check_mail_delay(id_course):
    send_mail_delay(id_course)
