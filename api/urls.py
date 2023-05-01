from django.urls import path, include
from . import views

urlpatterns = [
    path('user/create/', views.UserCreateView),
    path('user/login/', views.UserLoginView),
    path('user/logout/', views.UserLogoutView),
    path('user/gender/', views.updateGender),
    path('user/biometrics/', views.updateUserBiometrics),

    path('workout-plans/create/', views.create_workout_plan),
    path('exercise/finish/', views.finish_exercise),
    path('workout-plans/finish/', views.finish_workout_plan),

    # get all workout plans
    path('workout-plans/list/<str:hashed_id>/', views.list_user_workout_plans),
    
    # get all weeks of a workout plan
    path('workout-plans/<int:workout_id>/<str:hashed_id>/week/list/', views.list_workout_weeks),

    # get all workout days of a week
    path('workout-plans/week/<int:week_id>/<str:hashed_id>/day/list/', views.list_workout_days),

    # get all exercises of a day
    path('workout-plans/week/day/<int:day_id>/<str:hashed_id>/exercises/list/', views.list_workout_exercises),

    # updates the sets and reps of an exercises
    path('exercise/sets/', views.update_sets),
    path('exercise/reps/', views.update_reps)
]
