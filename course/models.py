from django.db import models

from users.models import User

NULLABLE = {'null': True, 'blank': True}

CASH = 'cash'
TRANSFER = 'transfer'
METHOD = [
    (CASH, 'Наличные'),
    (TRANSFER, 'Перевод на счет'),
]

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


class Payments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь', **NULLABLE)
    date_of_payment = models.DateField(verbose_name='дата платежа')
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, **NULLABLE)
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, **NULLABLE)
    payment_amount = models.IntegerField(verbose_name='сумма платежа')
    payment_method = models.CharField(max_length=50, choices=METHOD, verbose_name='метод оплаты')

    def __str__(self):
        return f'{self.paid_course if self.paid_course else self.paid_lesson} - {self.user}'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'
