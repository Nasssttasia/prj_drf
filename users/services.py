from users.models import User
from datetime import timedelta, datetime


def check_user():
    users = User.object.all()
    delta = datetime.now() - timedelta(days=30)
    for user in users:
        if user.last_login:
            if user.last_login.date() < delta.date():
                user.is_active = False
                user.save()


