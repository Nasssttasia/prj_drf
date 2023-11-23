from django.db import models

NULLABLE = {'null': True, 'blank': True}


class Course(models.Model):
    title = models.CharField(max_length=100, verbose_name='название курса')
    img = models.ImageField(upload_to='course_img/', verbose_name='аватарка', **NULLABLE)
    description = models.TextField(verbose_name='описание курса', **NULLABLE)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=100, verbose_name='название урока')
    description = models.TextField(verbose_name='описание урока', **NULLABLE)
    img = models.ImageField(upload_to='course_img/', verbose_name='аватарка', **NULLABLE)
    link = models.URLField(max_length=250, verbose_name='ссылка на видео')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
