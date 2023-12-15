from celery import shared_task

from users.services import check_user


@shared_task
def check_user_task():
    check_user()
