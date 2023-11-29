from django.core.management import BaseCommand

from course.models import Course


class Command(BaseCommand):

    def handle(self, *args, **options):
        course_list = [
            {'title': 'Курс 1', 'description': 'Интересный курс 1'},
            {'title': 'Курс 2', 'description': 'Увлекательный курс 2'}
        ]

        course_to_create = []
        for course in course_list:
            course_to_create.append(
                Course(**course)
            )

        Course.objects.bulk_create(course_to_create)
