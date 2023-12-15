from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from course.models import Lesson, Course, Subscription
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email='test@mail.ru',
            password='test',
            is_staff=True,
            is_superuser=True,
        )

        self.course = Course.objects.create(
            title='Test',
            user=self.user,
            description='text',
        )
        self.course.save()

        self.lesson = Lesson.objects.create(
            title='Test les',
            link='https://www.youtube.com/',
            description='text',
            course=self.course,
            user=self.user,
        )
        self.lesson.save()
        self.client.force_authenticate(user=self.user)

    def test_create_lesson(self):
        """Тест создания урока"""

        lesson = {
            'id': 1,
            'title': self.lesson.title,
            'description': self.lesson.description,
            'link': self.lesson.link,
            'course': self.lesson.course.id
        }

        response = self.client.post(
            reverse('course:lesson-create'),
            data=lesson
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            response.json(),
            {'id': 2, 'title': 'Test les', 'description': 'text', 'img': None, 'link': 'https://www.youtube.com/', 'user': None, 'course': 1}
        )
        self.assertTrue(
            Lesson.objects.all().exists()
        )

        response = self.client.get(
            '/lesson/',
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_update_lesson(self):
        """Тест изменения уроков"""

        lesson = {
            'id': 1,
            'title': 'update',
            'description': self.lesson.description,
            'link': self.lesson.link,
            'course': self.lesson.course.id
        }

        response = self.client.put(
            reverse('course:lesson-update', args=[self.lesson.pk]),
            data=lesson,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        '''self.assertEqual(
            response.json(),
            {'id': 1, 'title': 'test update update', 'description': 'test test', 'img': None, 'link': 'https://www.youtube.com/', 'user': None, 'course': 1}
        )'''

    def test_retrieve_lesson(self):
        """Тест удаления урока"""
        response = self.client.get(
            reverse('course:lesson-retrieve', args=[self.lesson.pk]),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_delete_lesson(self):
        """Тест удаления урока"""
        response = self.client.delete(
            reverse('course:lesson-delete', args=[self.lesson.pk]),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email='test@mail.ru',
            password='test',
            is_staff=True,
            is_superuser=True,
        )

        self.course = Course.objects.create(
            title='Test',
            user=self.user,
            description='text',
        )
        self.course.save()

        self.lesson = Lesson.objects.create(
            title='Test les',
            link='https://www.youtube.com/',
            description='text',
            course=self.course,
            user=self.user,
        )
        self.lesson.save()
        self.client.force_authenticate(user=self.user)

    def test_create_delete_subscription(self):
        """Тест создания подписки"""
        subscription = {
            'user': 1,
            'course': 1
        }

        response = self.client.post(
            reverse('course:subscription-create'),
            data=subscription
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertTrue(
            Subscription.objects.all().exists()
        )


        """Тест удаления подписки"""
        response = self.client.delete(
            reverse('course:subscription-delete', args=[self.lesson.pk]),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )