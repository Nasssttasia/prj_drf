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
            is_staff=True,
            is_superuser=True,
        )

        self.user.set_password('test')
        self.user.save()

        self.access_token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.course = Course(
            title='Test',
            user=self.user,
            description='text',
        )
        self.course.save()

    def test_create_lesson(self):
        """Тест создания урока"""

        lesson = {
            'title': 'test',
            'description': 'test test',
            'link': 'https://www.youtube.com/',
            'course': 1
        }

        response = self.client.post(
            '/lesson/create/',
            data=lesson
        )
        print(response.json())

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            response.json(),
            {'id': 1, 'title': 'test', 'description': 'test test', 'img': None, 'link': 'https://www.youtube.com/', 'user': None, 'course': 1}
        )
        self.assertTrue(
            Lesson.objects.all().exists()
        )

    def test_list_lesson(self):
        """Тест списка уроков"""

        lesson = {
            'title': 'test list',
            'description': 'test test list',
            'link': 'https://www.youtube.com/',
            'course': 1
        }

        self.client.post(
            '/lesson/create/',
            data=lesson
        )

        response = self.client.get(
            '/lesson/1/',
        )
        print(response.json())

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json(),
            {'id': 1, 'title': 'test list', 'description': 'test test list', 'img': None, 'link': 'https://www.youtube.com/', 'user': None, 'course': 1}
        )

    def test_update_lesson(self):
        """Тест изменения уроков"""

        lesson = {
            'title': 'test',
            'description': 'test test',
            'link': 'https://www.youtube.com/',
            'course': 1
        }

        self.client.post(
            '/lesson/create/',
            data=lesson,
            format='json'
        )

        response = self.client.patch(
            'lesson/update/1/',
            {'title': 'test update update'},
            format='json'
        )
        print(response.json())

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'id': 1, 'title': 'test update update', 'description': 'test test', 'img': None, 'link': 'https://www.youtube.com/', 'user': None, 'course': 1}
        )

    def test_delete_lesson(self):
        """Тест удаления урока"""
        response = self.client.delete(
            """ссылка на нужный объект"""
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email='test@mail.ru',
            is_staff=True,
            is_superuser=True,
        )

        self.user.set_password('test')
        self.user.save()

        self.access_token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.course = Course(
            title='Test',
            user=self.user,
            description='text',
        )
        self.course.save()

    def test_create_subscription(self):
        """Тест создания подписки"""
        subscription = {
            'user': 1,
            'course': 1
        }

        response = self.client.post(
            'subscription/create/',
            data=subscription
        )


        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertTrue(
            Subscription.objects.all().exists()
        )

    def test_delete_subscription(self):
        """Тест удаления подписки"""
        response = self.client.delete(
            """ссылка на нужный объект"""
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )