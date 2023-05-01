from django.contrib.auth.models import User
from .models import Exercise, Person, WorkoutPlan, User, WorkoutPlan, Week, Day, ExerciseSteps
from rest_framework import serializers

class PersonSerialize(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

class WorkoutPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutPlan
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    workout_plans = WorkoutPlanSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('__all__')

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = '__all__'

class ExerciseStepsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseSteps
        fields = '__all__'

class WeekSerializer(serializers.ModelSerializer):
    class Meta:
        model = Week
        fields = '__all__'

class DaySerializer(serializers.ModelSerializer):
    week = WeekSerializer()
    class Meta:
        model = Day
        fields = '__all__'

class WorkoutPlanSerializer(serializers.ModelSerializer):
    days = DaySerializer(many=True, read_only=True)
    class Meta:
        model = WorkoutPlan
        fields = '__all__'