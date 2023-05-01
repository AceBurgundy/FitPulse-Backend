from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Person(models.Model):
    """
    A user model representing a person who is participating in the workout program.

    Attributes:
        user (OneToOneField): One-to-one relationship with Django User model.
        hashed_id (CharField): Hashed ID of the user.
        gender (CharField): The gender of the user.
        height (FloatField): The height of the user.
        weight (FloatField): The weight of the user.

    Methods:
        __str__: Returns a string representation of the person in the format 

    Extending User(<user.id>) as Person with attributes
        hashed_id <hashed_id>,
        gender <gender>,
        height <height>,
        weight <weight>\n
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hashed_id = models.CharField(max_length=64)
    gender = models.CharField(max_length=10)
    height = models.FloatField()
    weight = models.FloatField()

    def __str__(self):
        
        return f"""
    Extending User({self.user.id}) as Person with attributes
        hashed_id {self.hashed_id},
        gender {self.gender},
        height {self.height},
        weight {self.weight}\n
    """

class WorkoutPlan(models.Model):
    """
    A model representing a workout plan for a user.

    Attributes:
        person (ForeignKey): The user who the workout plan belongs to.
        name (CharField): The name of the workout plan.
        number (IntegerField): The number of the workout plan
        started (BooleanField): Indicates whether the workout plan has been started.
        finished (BooleanField): Indicates whether the workout plan has been completed.
        date_created (DateTimeField): The date and time when the workout plan was created.

    Methods:
        __str__: Returns a string representation of the workout plan in the format "<username>'s workout plan <number>".
    """
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    number = models.IntegerField()
    started = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.person.user.username}'s workout plan {self.number}"

    class Meta:
        get_latest_by = "date_created"

class Week(models.Model):
    """
    A model representing a week of a workout plan.

    Attributes:
        workout_plan (ForeignKey): The workout plan the week belongs to.
        number (IntegerField): The number of the week within the workout plan.
        current_week (BooleanField): Indicates whether the week is the current exercise week.
        finished (BooleanField): Indicates whether the week has been completed.

    Methods:
        get_next: Returns the next week instance, if it exists.
        has_next: Returns True if the next week instance exists, False otherwise.
        set_next_as_current: Sets the next week instance as the current week.

        __str__ method returns a string representation of the week in the format "Week <number> from <workout_plan> with a <finished_status> status".
    """
    workout_plan = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE)
    number = models.IntegerField()
    current_week = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def get_next(self):
        return self.__class__.objects.filter(id__gt=self.id).order_by('id').first()
    
    def has_next(self):
        return self.get_next() is not None
    
    def set_next_as_current(self):
        next_week = self.get_next()
        if next_week is not None:
            # Set current week's "current_week" field to False
            self.current_week = False
            self.save()
            
            # Set next week's "current_week" field to True
            next_week.current_week = True
            next_week.save()
    
    def __str__(self):
        return f"Week {self.number} from {self.workout_plan} with a {'finished' if self.finished else 'unfinished'} status"

    class Meta:
        get_latest_by = "date_created"

class Day(models.Model):
    """
    A model representing a day of a week within a workout plan.

    Attributes:
        week (ForeignKey): The week the day belongs to.
        number (IntegerField): The number of the day within the week.
        name (CharField): The name of the day.
        finished (BooleanField): Indicates whether the day has been completed.

    Methods:
        __str__: Returns a string representation of the day in the format "Day <day_number> of <week> with a <finished_status> status".
    """
    week = models.ForeignKey(Week, on_delete=models.CASCADE)
    number = models.IntegerField()
    name = models.CharField(max_length=9)
    finished = models.BooleanField(default=False)

    def __str__(self):
        return f"Day {self.day_number} of {self.week} with a {'finished' if self.finished else 'unfinished'} status"

class Exercise(models.Model):
    """
    A model representing an exercise within a day of a week within a workout plan.

    Attributes:
        day (ForeignKey): The day the exercise belongs to.
        name (CharField): The name of the exercise.
        description (TextField): A description of the exercise.
        finished (BooleanField): Indicates whether the exercise has been completed.
        reps (IntegerField): The number of reps for the exercise. Optional.
        sets (IntegerField): The number of sets for the exercise. Optional.
        time_based (BooleanField): Indicates whether the exercise is time-based. Default is False.
        time (CharField): The duration of the exercise in minutes or seconds. Optional.
        no_time_limit (BooleanField): Indicates whether there is no time limit for the exercise. Default is False.
        link (URLField): A link to the exercise demonstration or instructions.

    Methods:
        __str__: Returns a string representation of the exercise in the format "<day>: <name> (<reps> reps x <sets> sets)".
    """
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    finished = models.BooleanField(default=False)
    reps = models.IntegerField(null=True)
    sets = models.IntegerField(null=True)
    time_based = models.BooleanField(default=False)
    time = models.CharField(max_length=30, null=True)
    no_time_limit = models.BooleanField(default=False)
    link = models.URLField()

    def __str__(self):
        return f'{self.day}: {self.name} ({self.reps} reps x {self.sets} sets)'

class ExerciseSteps(models.Model):
    """
    A step for an exercise in a workout plan.

    Attributes:
        exercise (ForeignKey): The exercise that this step belongs to.
        instruction (CharField): The description of the step.

    Methods:
        __str__: Returns a string representation of the step in the format "<exercise>: <step>".
    """
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    instruction = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.exercise}: {self.instruction}'