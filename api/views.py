from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Exercise, ExerciseSteps, Person, WorkoutPlan, Day, Week, WorkoutPlan
from .serializers import DaySerializer, ExerciseSerializer, ExerciseStepsSerializer, UserSerializer, WeekSerializer, WorkoutPlanSerializer
from .utils import Workout
import hashlib

def authenticate_user(view_func):
    def wrapper(request, *args, **kwargs):

        hashed_id = request.data.get('X-User-Id')
        if not hashed_id:
            return Response({'error': 'User was not provided'}, status=status.HTTP_400_BAD_REQUEST)

        person = Person.objects.filter(hashed_id=hashed_id).first()
        if not person.user or not person:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if not person.user.is_authenticated:
            return Response({'error': 'User not logged in'}, status=status.HTTP_401_UNAUTHORIZED)

        return view_func(request, *args, **kwargs)

    return wrapper

# -----------------------------------Route for login and registration-------------------------------

@api_view(['POST'])
def UserCreateView(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():

        password = request.data.get('password')
        if not password:
            return Response({'error': 'Password not provided'}, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save(password=make_password(password))
        user.save()

        Person.objects.create(hashed_id=hashlib.sha256(str(user.id).encode()).hexdigest(), user=user, gender="", height=0, weight=0)
        
        return Response({'success': True}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def UserLoginView(request):

    username = request.data.get('username')
    if not username:
        return Response({'error': 'Username not provided'}, status=status.HTTP_400_BAD_REQUEST)

    password = request.data.get('password')
    if not password:
        return Response({'error': 'Password not provided'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(request, username=username, password=password)
        
    if user is not None:
        has_workout_plans = WorkoutPlan.objects.filter(person=user.person.id).exists()
        hashed_id = user.person.hashed_id
        login(request, user)
        return Response({'success': True, 'userHashedId': hashed_id, 'hasWorkoutPlans' : has_workout_plans}, status=status.HTTP_200_OK)
    else:
        return Response({'error': ['Invalid username or password', 'Registration needed']}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@authenticate_user
def UserLogoutView(request):
    
    hashed_id = request.data.get('X-User-Id')
    person = Person.objects.filter(hashed_id=hashed_id).first()

    user = person.user

    if user:
        logout(request)
        return Response({'success': 'User logged out successfully.'}, status=200)
    
    return Response({'error': 'User not found or not logged in.'}, status=404)

# -------------------------------Route for updating Person attributes--------------------------------

@api_view(["PUT"])
@authenticate_user
def updateGender(request):

    hashed_id = request.data.get('X-User-Id')

    person = Person.objects.filter(hashed_id=hashed_id).first()

    gender = request.data.get('gender', None)
    if gender is None:
        return Response({'error': 'User has not selected a gender'}, status=status.HTTP_400_BAD_REQUEST)
    
    person.gender = gender
    person.save()

    return Response({'success': True}, status=status.HTTP_200_OK)

@api_view(["PUT"])
@authenticate_user
def updateUserBiometrics(request):

    hashed_id = request.data.get('X-User-Id')

    person = Person.objects.filter(hashed_id=hashed_id).first()

    height = request.data.get('userHeight', None)
    if height is None:
        return Response({'error': 'Height was not provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    weight = request.data.get('userWeight', None)
    if weight is None:
        return Response({'error': 'Weight was not provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    person.height = height
    person.weight = weight
    person.save()

    return Response({'success': True}, status=status.HTTP_200_OK)

# -----------------------------Routes for creating and displaying workout data---------------------------------

@api_view(['POST'])
@authenticate_user
def create_workout_plan(request):
    """
    A view that creates a new workout plan for a user.
    """
    hashed_id = request.data.get('X-User-Id')

    person = Person.objects.filter(hashed_id=hashed_id).first()

    preferred_days = request.data.get('preferredDays', None)
    if preferred_days is None:
        return Response({'error': 'Preferred days are empty'}, status=status.HTTP_404_NOT_FOUND)

    workout_plan_create = Workout().generate_workout_plan(person, preferred_days)
    if not workout_plan_create:
        return Response({'error': 'Workout Plan Not Created'}, status=status.HTTP_404_NOT_FOUND)

    return Response({'success': 'New Workout Plan created'}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def list_user_workout_plans(request, hashed_id):
    """
    A view that lists all workout plans for a user.
    """
    person = Person.objects.filter(hashed_id=hashed_id).first()
    if not person:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if not person.user.is_authenticated:
        return Response({'error': 'User not logged in'}, status=status.HTTP_401_UNAUTHORIZED)

    workout_plans = WorkoutPlan.objects.filter(person=person)
    if not workout_plans:
        return Response({'error': 'Workout plans not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = WorkoutPlanSerializer(workout_plans, many=True)

    return Response({
        'data': serializer.data,
        'gender': person.gender,
        'workouts_completed': all(workout_plan.finished for workout_plan in workout_plans),
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
def list_workout_weeks(request, workout_id, hashed_id):
    """
    A view that lists all weeks related to a workout plan
    """
    person = Person.objects.filter(hashed_id=hashed_id).first()
    if not person:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if not person.user.is_authenticated:
        return Response({'error': 'User not logged in'}, status=status.HTTP_401_UNAUTHORIZED)

    if not workout_id:
        return Response({'error': 'Workout not provided'}, status=status.HTTP_404_NOT_FOUND)

    workout = WorkoutPlan.objects.filter(id=workout_id).first()
    # starts workout when user accesses its weeks content
    workout.started = True
    workout.save()

    workout_weeks = Week.objects.filter(workout_plan=workout_id)
    if not workout_weeks:
        return Response({'error': 'Workout weeks not found'}, status=status.HTTP_404_NOT_FOUND)

    for week in workout_weeks:
        if not week.finished:
            break
    else:
        workout.finished = True
        workout.save()

    serializer = WeekSerializer(workout_weeks, many=True)
    return Response({'data' : serializer.data, 'gender' : person.gender, 'workoutName' : workout.name}, status=status.HTTP_200_OK)

@api_view(['GET'])
def list_workout_days(request, week_id, hashed_id):
    """
    A view that lists all days related to workout week
    """
    person = Person.objects.filter(hashed_id=hashed_id).first()
    if not person:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if not person.user.is_authenticated:
        return Response({'error': 'User not logged in'}, status=status.HTTP_401_UNAUTHORIZED)

    if not week_id:
        return Response({'error': 'Week not provided'}, status=status.HTTP_404_NOT_FOUND)

    week = Week.objects.filter(id=week_id).first()
    if not week:
        return Response({'error': 'Week not found'}, status=status.HTTP_404_NOT_FOUND)

    day = Day.objects.filter(week=week_id).order_by('number')
    if not day:
        return Response({'error': 'No day found for the given week'}, status=status.HTTP_404_NOT_FOUND)

    for current_day in day:
        if not current_day.finished:
            break
    else:
        week.finished = True
        if week.has_next():
            week.set_next_as_current()
        week.save()

    serializer = DaySerializer(day, many=True)
    return Response({'data' : serializer.data, 'gender' : person.gender }, status=status.HTTP_200_OK)


@api_view(['GET'])
def list_workout_exercises(request, day_id, hashed_id):
    """
    A view that lists all exercises related to workout day
    """
    person = Person.objects.filter(hashed_id=hashed_id).first()
    if not person:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if not person.user.is_authenticated:
        return Response({'error': 'User not logged in'}, status=status.HTTP_401_UNAUTHORIZED)

    if not day_id:
        return Response({'error': 'Day not provided'}, status=status.HTTP_404_NOT_FOUND)

    day = Day.objects.filter(id=day_id).first()
    exercises = Exercise.objects.filter(day=day_id)
    if not exercises:
        return Response({'error': 'No exercise found for the given day'}, status=status.HTTP_404_NOT_FOUND)

    exercise_list = []
    for exercise in exercises:
        exercise_data = ExerciseSerializer(exercise).data
        steps = ExerciseSteps.objects.filter(exercise=exercise)
        if steps:
            exercise_data['steps'] = [step.instruction for step in steps]
        else:
            exercise_data['steps'] = []
        exercise_list.append(exercise_data)

    return Response({'data' : exercise_list, 'gender' : person.gender, 'dayName' : day.name}, status=status.HTTP_200_OK)

@api_view(['GET'])
def list_workout_exercise_steps(request, exercise_id, hashed_id):
    """
    A view that lists all exercises_step related to an exercise
    """
    person = Person.objects.filter(hashed_id=hashed_id).first()
    if not person:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if not person.user.is_authenticated:
        return Response({'error': 'User not logged in'}, status=status.HTTP_401_UNAUTHORIZED)

    if not exercise_id:
        return Response({'error': 'Exercise not provided'}, status=status.HTTP_404_NOT_FOUND)

    exercise_steps = ExerciseSteps.objects.filter(exercise=exercise_id)
    if not exercise_steps:
        return Response({'error': 'No steps found for the given exercise'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ExerciseStepsSerializer(exercise_steps, many=True)
    return Response({'data' : serializer.data}, status=status.HTTP_200_OK)

# -----------------------------Routes for updating reps and sets of an exercise-------------------

@api_view(['PUT'])
@authenticate_user
def update_reps(request):
    """
    A view that updates the reps for an exercise.
    """
    exercise_id = request.data.get("exercise_id")
    if not exercise_id:
        return Response({'error': 'Exercise was not provided'}, status=status.HTTP_404_NOT_FOUND)

    exercise = Exercise.objects.filter(id=exercise_id).first()
    if not exercise:
        return Response({'error': 'Exercise does not exist'}, status=status.HTTP_404_NOT_FOUND)

    reps = request.data.get('reps', None)
    if not reps:
        return Response({'error': 'Reps not provided'}, status=status.HTTP_400_BAD_REQUEST)

    exercise.reps = reps
    exercise.save()

    return Response({'success': 'Reps updated'}, status=status.HTTP_200_OK)

@api_view(['PUT'])
@authenticate_user
def update_sets(request):
    """
    A view that updates the sets for an exercise.
    """
    exercise_id = request.data.get("exercise_id")
    if not exercise_id:
        return Response({'error': 'Exercise was not provided'}, status=status.HTTP_404_NOT_FOUND)

    exercise = Exercise.objects.filter(id=exercise_id).first()
    if not exercise:
        return Response({'error': 'Exercise does not exist'}, status=status.HTTP_404_NOT_FOUND)

    sets = request.data.get('sets', None)

    if not sets:
        return Response({'error': 'Sets not provided'}, status=status.HTTP_400_BAD_REQUEST)

    exercise.sets = sets
    exercise.save()

    return Response({'success': 'Sets updated'}, status=status.HTTP_200_OK)

# -----------------------------Routes for setting finished status---------------------------------

@api_view(['PUT'])
@authenticate_user
def finish_exercise(request):
    """
    A view that sets the 'finished' attribute of an exercise to True.
    """
    exercise_id = request.data.get("exercise_id")
    if not exercise_id:
        return Response({'error': 'Exercise was not provided'}, status=status.HTTP_404_NOT_FOUND)

    exercise = Exercise.objects.filter(id=exercise_id).first()
    if not exercise:
        return Response({'error': 'Exercise does not exist'}, status=status.HTTP_404_NOT_FOUND)

    exercise.finished = True
    exercise.save()

    day = exercise.day
    for exercise in day.exercise_set.all():
        if not exercise.finished:
            break
    else:
        day.finished = True
        day.save()

    return Response({'success': 'Exercise completed'}, status=status.HTTP_200_OK)

@api_view(['PUT'])
@authenticate_user
def finish_workout_plan(request):
    """
    A view that sets the 'finished' attribute of a workout plan to True.
    """
    workout_plan_id = request.data.get("workout_plan_id")
    if not workout_plan_id:
        return Response({'error': 'Workout plan was not provided'}, status=status.HTTP_404_NOT_FOUND)

    workout_plan = WorkoutPlan.objects.filter(id=workout_plan_id).first()
    if not workout_plan:
        return Response({'error': 'Workout plan does not exist'}, status=status.HTTP_404_NOT_FOUND)

    workout_plan.finished = True
    workout_plan.save()

    return Response({'success': 'Workout plan completed'}, status=status.HTTP_200_OK)
