from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin@sky.pro',
            first_name='Admin',
            last_name='SkyPro',
            is_staff=True,
            is_superuser=True,
            is_active=True
        )

        user.set_password('ad123min')
        user.save()



self.assertEqual(
            response.json(),
            {'id': 1, 'title': 'test', 'description': 'test test', 'img': None, 'link': 'https://www.youtube.com/',
             'user': None, 'course': 1}
        )