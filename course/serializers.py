from rest_framework import serializers

from course.models import Course, Lesson, Payments, Subscription
from course.validators import YouTubeLink


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [YouTubeLink(field='link')]


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lesson = LessonSerializer(many=True, read_only=True)
    subscription = serializers.SerializerMethodField()

    def get_lessons_count(self, instance):
        if instance.lesson_set.all():
            return instance.lesson_set.all().count()
        return 0

    def get_subscription(self, instance):
        request = self.context.get('request')
        if request:
            return instance.subscription_set.filter(user=request.user).exists()
        return False

    class Meta:
        model = Course
        fields = '__all__'


class PaymentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payments
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = '__all__'
