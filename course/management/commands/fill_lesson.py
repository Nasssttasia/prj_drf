from django.core.management import BaseCommand

from course.models import Lesson


class Command(BaseCommand):

    def handle(self, *args, **options):
        lesson_list = [
            {'title': 'Урок 1', 'description': 'Интересный урок 1', 'link': 'https://my.sky.pro/student-cabinet/stream-lesson/36088/theory/3'},
            {'title': 'Урок 2', 'description': 'Увлекательный урок 2', 'link': 'https://my.sky.pro/student-cabinet/stream-lesson/36088/theory/3'}
        ]

        lesson_to_create = []
        for lesson in lesson_list:
            lesson_to_create.append(
                Lesson(**lesson)
            )

        Lesson.objects.bulk_create(lesson_to_create)
