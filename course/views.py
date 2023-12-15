import stripe
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from course.models import Course, Lesson, Payments, Subscription
from course.paginators import CoursePaginator
from course.permissions import IsUsers, IsOwnerOrStaff
from course.serializers import CourseSerializer, LessonSerializer, PaymentsSerializer, SubscriptionSerializer
from course.tasks import check_mail_delay


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CoursePaginator

    def update(self, request, *args, **kwargs):
        check_mail_delay.delay(kwargs['pk'])
        return super().update(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user)
        return queryset

    def get_permissions(self):
        if self.action == 'create' or self.action == 'destroy':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsOwnerOrStaff, IsAuthenticated]
        return [permission() for permission in permission_classes]


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrStaff]
    pagination_class = CoursePaginator

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrStaff]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrStaff]

    '''id_course = Lesson.objects.course.pk
    check_mail_delay.delay(id_course)'''


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsUsers]


class PaymentsCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentsSerializer
    permission_classes = [IsAuthenticated]

    def payment_create(self, serializer):
        payment = serializer.save()
        stripe.api_key = 'sk_test_51OMYTLIPYT4aN48f1Sx8tKPiiZmA9RkBN5L8OSmLu9q5HtBl6jqUuhoOe8oD1haMMISnQQmJhshVPZ8BFzUhKxiU00gGzlmXOo'
        pay = stripe.PaymentIntent.create(
            amount=payment.payment_amount,
            currency='usd',
            automatic_payment_methods={'enabled': True}
        )
        payment = serializer.save(payment_id=pay['id'])
        return super().perform_create(serializer)


class PaymentsListAPIView(generics.ListAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('paid_course', 'paid_lesson', 'payment_method',)
    ordering_fields = ('date_of_payment',)


class PaymentsRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrStaff]

    def get_payment(self, payment_id):
        stripe.api_key = 'sk_test_51OMYTLIPYT4aN48f1Sx8tKPiiZmA9RkBN5L8OSmLu9q5HtBl6jqUuhoOe8oD1haMMISnQQmJhshVPZ8BFzUhKxiU00gGzlmXOo'
        payment = stripe.PaymentIntent.retrieve(payment_id)
        return Response({
            'status': payment.status,
            'body': payment})


class SubscriptionCreateAPIView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated]
