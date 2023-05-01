from .models import Exercise, Day, Week, WorkoutPlan, ExerciseSteps
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
import random

class Workout():
 
    def __init__(self):
        """
        Initialize a `WorkoutPlanner` class instance.
        
        The `_exercises` dictionary contains a collection of exercise information including descriptions, 
        recommended duration, and steps to complete the exercise. The `__days_of_the_week` list contains 
        the days of the week. 
        """

        self._exercises = {

            "Bridge": {
                "description": "The bridge is a great exercise to target your glutes, hamstrings, and lower back.",
                "time": True,
                "duration": "1 minute",
                "steps": {
                    "1": "Lie on your back with your knees bent and feet flat on the ground.",
                    "2": "Lift your hips up towards the ceiling, keeping your shoulders and feet grounded.",
                    "3": "Hold for a few seconds before lowering back down."
                },
            "link" : "https://www.youtube.com/embed/Fctxa_BBjds"
            },

            "Chair squat": {
                "description": "The chair squat is a lower-body exercise that targets your quadriceps, hamstrings, and glutes.",
                "steps": {
                    "1": "Stand with your feet hip-width apart.",
                    "2": "Squat down as if you're sitting in a chair, keeping your weight on your heels and your knees behind your toes.",
                    "3": "Rise back up to standing and repeat."
                },
            "link" : "https://www.youtube.com/embed/4k1SPQ9tEMg"
            },

            "Knee pushup": {
                "description": "The knee pushup is a modification of the traditional pushup that is easier to perform.",
                "steps": {
                    "1": "Start in a plank position with your hands and knees on the ground.",
                    "2": "Lower your chest towards the ground by bending your elbows.",
                    "3": "Push back up to the starting position."
                },
            "link" : "https://www.youtube.com/embed/jWxvty2KROs"
            },

            "Stationary lunge": {
                "description": "The stationary lunge is a great exercise to target your quadriceps, hamstrings, and glutes.",
                "steps": {
                    "1": "Stand with one foot forward and the other foot back, with your feet hip-width apart.",
                    "2": "Bend your front knee to lower your body towards the ground, keeping your back straight.",
                    "3": "Rise back up and repeat on the other side."
                },
            "link" : "https://www.youtube.com/embed/qO_21ExL4zw"
            },

            "Plank to Downward Dog": {
                "description": "The plank to downward dog is a great exercise to stretch your hamstrings, calves, and back.",
                "time": True,
                "duration": "30-60 seconds",
                "steps": {
                    "1": "Start in a plank position with your arms straight and your body in a straight line.",
                    "2": "Push your hips up towards the ceiling to move into a downward dog position.",
                    "3": "Return to plank and repeat."
                },
            "link" : "https://www.youtube.com/embed/J8QhVr5Pvig"
            },

            "Straight-leg donkey kick": {
                "description": "The straight-leg donkey kick is an exercise that targets your glutes and hamstrings.",
                "steps": {
                    "1": "Start on all fours with your hands and knees on the ground.",
                    "2": "Keeping your leg straight, lift one leg up behind you until it's in line with your body.",
                    "3": "Lower back down and repeat on the other side."
                },
            "link" : "https://www.youtube.com/embed/FlWTMfgB0Hk"
            },

            "Bird Dog": {
                "description": "The bird dog is an exercise that targets your lower back, glutes, and abs.",
                "steps": {
                    "1": "Start on all fours with your hands and knees on the ground.",
                    "2": "Lift one arm and the opposite leg straight out from your body, keeping your back straight.",
                    "3": "Lower back down and repeat on the other side."
                },
            "link" : "https://www.youtube.com/embed/wiFNA3sqjCA"
            },

            "Side-lying hip abduction": {
                "description": "The side-lying hip abduction is an exercise that targets your glutes and outer thigh muscles.",
                "steps": {
                    "1": "Lie on your side with your legs straight and stacked on top of each other.",
                    "2": "Lift your top leg as high as you can without moving your hips.",
                    "3": "Lower back down and repeat on the other side."
                },
            "link" : "https://www.youtube.com/embed/RwH43Qdgcbo"
            },

            "Bicycle crunch": {
                "description": "The bicycle crunch is an exercise that targets your abs and oblique muscles.",
                "steps": {
                    "1": "Lie on your back with your hands behind your head and your knees bent.",
                    "2": "Lift your shoulder blades off the ground and bring your left elbow to your right knee while straightening your left leg.",
                    "3": "Switch sides and repeat."
                },
            "link" : "https://www.youtube.com/embed/Iwyvozckjak"
            },

            "Pushups": {
                "description": "A classic bodyweight exercise that targets your chest, triceps, and shoulders.",
                "steps": {
                    "1": "Assume a plank position with your hands slightly wider than shoulder-width apart and your feet close together",
                    "2": "Lower your body by bending your elbows and keeping your back straight",
                    "3": "Stop when your chest is just above the ground",
                    "4": "Push yourself back up to the starting position",
                    "5": "Repeat for desired number of reps"
                },
            "link" : "https://www.youtube.com/embed/JyCG_5l3XLk"
            },
            
            "Squats": {
                "description": "A lower body exercise that targets your quadriceps, hamstrings, and glutes.",
                "steps": {
                    "1": "Stand with your feet shoulder-width apart and your toes pointing straight ahead",
                    "2": "Bend your knees and push your hips back as if you were going to sit down on a chair",
                    "3": "Keep your weight on your heels and your chest lifted",
                    "4": "Lower your body until your thighs are parallel to the ground",
                    "5": "Push yourself back up to the starting position",
                    "6": "Repeat for the instructed number of reps"
                },
            "link" : "https://www.youtube.com/embed/xqvCmoLULNY"
            },
            
            "Plank": {
                "description": "A core exercise that targets your abs, back, and shoulder muscles.",
                "time": True,
                "duration": "30 seconds - 1 minute",
                "steps": {
                    "1": "Assume a plank position with your forearms on the ground, elbows directly under your shoulders, and your feet hip-width apart",
                    "2": "Keep your body in a straight line from head to heels, engaging your core muscles to prevent your hips from sagging",
                    "3": "Hold the position for the 30 seconds - 1 minute",
                    "4": "Release and rest",
                },
            "link" : "https://www.youtube.com/embed/ASdvN_XEl_c"
            },
            
            "Burpees": {
                "description": "A full-body exercise that targets your chest, arms, legs, and core muscles.",
                "steps": {
                    "1": "Stand with your feet hip-width apart and your arms at your sides",
                    "2": "Lower your body into a squat position and place your hands on the ground in front of you",
                    "3": "Kick your legs back into a pushup position",
                    "4": "Perform a pushup",
                    "5": "Jump your feet back up towards your hands",
                    "6": "Stand up and jump as high as you can",
                    "7": "Repeat for the required number of reps"
                },
            "link" : "https://www.youtube.com/embed/TU8QYVW0gDU"
            },
            
            "Crunches": {
                "description": "A core exercise that targets your abs.",
                "steps": {
                    "1": "Lie on your back with your knees bent and your feet flat on the ground",
                    "2": "Place your hands behind your head or across your chest",
                    "3": "Lift your shoulders off the ground by contracting your abs",
                    "4": "Pause briefly at the top of the movement",
                    "5": "Lower your shoulders back down to the ground",
                    "6": "Repeat for desired number of reps"
                },
            "link" : "https://www.youtube.com/embed/Xyd_fa5zoEU"
            },
            
            "Mountain climbers": {
                "description": "A full-body exercise that targets your abs, arms, and legs.",
                "steps": {
                    "1": "Assume a plank position with your hands directly under your shoulders and your feet hip-width apart",
                    "2": "Lift one foot off the ground and bring your knee towards your chest, keeping your core engaged",
                    "3": "Quickly switch to the other foot and bring your knee towards your chest",
                    "4": "Continue alternating legs in a running-like motion, while keeping your upper body stable",
                    "5": "Increase speed for more intensity",
                    "6": "Repeat for desired number of reps"
                },
            "link" : "https://www.youtube.com/embed/nmwgirgXLYM"
            },
            
            "Jumping jacks": {
                "description": "A full-body exercise that increases your heart rate and improves coordination.",
                "steps": {
                    "1": "Stand with your feet together and your arms at your sides",
                    "2": "Jump your feet out to the sides and raise your arms above your head at the same time",
                    "3": "Jump your feet back together and lower your arms to your sides",
                    "4": "Repeat for desired number of reps"
                },
            "link" : "https://www.youtube.com/embed/iSSAk4XCsRA"
            },
            
            "Jumping lunges": {
            "description": "A challenging exercise that targets your legs, glutes, and core.",
            "steps": {
                    "1": "Start in a lunge position with your right leg forward and your left leg back, both knees bent at 90 degrees.",
                    "2": "Jump up explosively and switch your leg position in midair, landing in a lunge position with your left leg forward.",
                    "3": "Continue alternating legs as fast as possible for desired number of reps."
                },
            "link" : "https://www.youtube.com/embed/hTdcOG9muQk"
            },

            "Tricep dips": {
            "description": "An exercise that targets your triceps, shoulders, and chest, and can be done using a chair or bench.",
            "steps": {
                    "1": "Sit on the edge of a chair or bench with your hands resting on the edge, fingers pointing forward.",
                    "2": "Slide your butt off the edge and lower your body towards the ground by bending your elbows.",
                    "3": "Push yourself back up to the starting position and repeat for desired number of reps."
                },
            "link" : "https://www.youtube.com/embed/0326dy_-CzM"
            },

            "Russian twists": {
            "description": "An exercise that targets your abs and obliques.",
            "steps": {
                    "1": "Sit on the ground with your knees bent and feet flat on the ground, leaning your torso back slightly.",
                    "2": "Clasp your hands together in front of your chest and twist your torso to the right, tapping your hands on the ground.",
                    "3": "Twist to the left and tap the ground on the opposite side.",
                    "4": "Continue alternating sides for desired number of reps."
                },
            "link" : "https://www.youtube.com/embed/wkD8rjkodUI"
            },

            "Plank shoulder taps": {
            "description": "An exercise that targets your abs, shoulders, and upper back.",
            "steps": {
                    "1": "Start in a plank position with your arms straight and your body in a straight line.",
                    "2": "Lift your right hand and tap your left shoulder, then return it to the ground.",
                    "3": "Lift your left hand and tap your right shoulder, then return it to the ground.",
                    "4": "Continue alternating sides for desired number of reps."
                },
            "link" : "https://www.youtube.com/embed/ztpXZm7Dv80"
            },

            "Jump rope": {
            "description": "A fun and simple exercise that provides a great cardio workout while improving coordination and balance.",
            "time" : True,
            "no_time_limit": True,
            "steps": {
                    "1": "Stand with your feet hip-width apart, holding a jump rope by the handles with both hands.",
                    "2": "Swing the rope over your head and jump as it passes under your feet.",
                    "3": "Land softly on the balls of your feet and repeat for desired number of reps."
                },
            "link" : "https://www.youtube.com/embed/u3zgHI8QnqE"
            },

            "Wall sit": {
            "description": "A lower body exercise that targets your quadriceps, hamstrings, and glutes.",
            "time" : True,
            "no_time_limit": True,
            "steps": {
                    "1": "Stand with your back against a wall and your feet shoulder-width apart.",
                    "2": "Slide down the wall until your thighs are parallel to the ground, with your knees directly above your ankles.",
                    "3": "Hold this position for as long as you can, keeping your back straight and your abs engaged."
                },
            "link" : "https://www.youtube.com/embed/XULOKw4E4P4"
            },

            "Superman": {
            "description": "An exercise that targets your lower back, glutes, and shoulders.",
            "time" : True,
            "duration": "1 minute",
            "steps": {
                    "1": "Lie face down on a mat with your arms and legs extended.",
                    "2": "Lift your arms, chest, and legs off the ground, keeping your neck in a neutral position.",
                    "3": "Hold for a few seconds before lowering back down to the starting position."
                },
            "link" : "https://www.youtube.com/embed/J9zXkxUAfUA"
            },

            "Single-Leg Deadlift": {
            "description": "A unilateral exercise that strengthens your hamstrings, glutes, and lower back.",
            "steps": {
                    "1": "Stand with your feet hip-width apart, holding a dumbbell in one hand.",
                    "2": "Lift one foot slightly off the ground and hinge forward at your hips, extending your lifted leg behind you.",
                    "3": "Lower the weight down towards the ground while keeping your back straight and your lifted leg parallel to the floor.",
                    "4": "Return to standing, squeezing your glutes and driving your hips forward, then repeat on the other side for desired number of reps."
                },
            "link" : "https://www.youtube.com/embed/HtHxnWmMgzM"
            },

            "Reverse Lunges with Knee Lift": {
            "description": "A lower body exercise that strengthens your legs and improves balance and stability.",
            "steps": {
                    "1": "Stand with your feet hip-width apart and take a big step back with one foot, bending both knees to lower your body down into a lunge.",
                    "2": "Press through your front foot to return to standing, lifting your back leg and raising your knee up towards your chest.",
                    "3": "Lower your foot back down to the ground and step back into a lunge on the same side.",
                    "4": "Repeat on the other side for desired number of reps."
                },
            "link" : "https://www.youtube.com/embed/extwj0TKGX8"
            },

            "Bear Crawl": {
            "description": "A full-body exercise that strengthens your core, shoulders, and hips.",
            "steps": {
                    "1": "Start in a plank position with your hands and feet on the ground, wrists directly under your shoulders.",
                    "2": "Step your right hand and left foot forward at the same time, keeping your hips low and your knees hovering just above the ground.",
                    "3": "Step your left hand and right foot forward at the same time, moving forwards and keeping your core engaged.",
                    "4": "Reverse the movement by stepping your right foot and left hand back, then your left foot and right hand, returning to the starting position. Repeat for desired number of reps."
                },
            "link" : "https://www.youtube.com/embed/t8XLor7unqU"
            },

            "Shoulder Taps with Leg Raise": {
            "description": "An upper body and core exercise that improves shoulder stability and strengthens your abs.",
            "steps": {
                    "1": "Start in a plank position with your hands on the ground shoulder-width apart and your feet hip-width apart.",
                    "2": "Lift your right hand to tap your left shoulder, keeping your core tight to prevent your hips from rotating.",
                    "3": "Lift your right leg up towards the ceiling, squeezing your glutes and keeping your hips level.",
                    "4": "Lower your leg and hand back to the starting position, then repeat on the other side for desired number of reps."
                },
            "link" : "https://www.youtube.com/embed/QDQKV9QtwUA"
            },

            "Bulgarian Split Squat": {
            "description": "A lower body exercise that strengthens the legs, glutes, and core while improving balance and stability.",
            "steps": {
                    "1": "Stand with your feet hip-width apart, facing away from a bench or step.",
                    "2": "Extend your left leg behind you and place the top of your left foot on the bench or step.",
                    "3": "Lower your body down towards the ground, bending your right knee and keeping your left leg straight.",
                    "4": "Press through your right heel to stand back up to the starting position, then repeat for desired number of reps before switching legs."
            },
            "link": "https://www.youtube.com/embed/2C-uNgKwPLE"
            }

        }

        self.__days_of_the_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
    def _calculate_bmi(self, person):
        """
        Calculates the body mass index (BMI) of the person based on their weight and height.

        Args:
            person: A User instance with a weight and height.

        Returns:
            The BMI of the person as a float.
        """
        # Calculate BMI
        bmi = person.weight / (person.height ** 2)
        return bmi

    def _determine_sets_and_reps(self, person, bmi):
        """
        Determines the recommended sets and reps for each exercise based on the person's gender and BMI.

        Args:
            person: A User instance.
            bmi: The body mass index (BMI) of the person.

        Returns:
            A tuple containing the recommended number of sets and reps as integers.
        """
        if person.gender.lower() == "male":
            if bmi < 18.5:
                sets = 3
                reps = 12
            elif bmi < 25:
                sets = 4
                reps = 10
            else:
                sets = 5
                reps = 8

        if person.gender.lower() == "female":
            if bmi < 18.5:
                sets = 2
                reps = 15
            elif bmi < 25:
                sets = 3
                reps = 12
            else:
                sets = 4
                reps = 10

        return sets, reps

    def _determine_num_weeks(self, preferred_days):
        """
        Determines the number of weeks for the workout plan based on the person's preferred workout days.

        Args:
            person: A User instance with a preferred_days attribute.

        Returns:
            The recommended number of weeks as an integer.
        """
        num_days = len(preferred_days)
        num_weeks = 4  # Set a default value of 12 weeks
        while num_days * num_weeks < 0.25 * 365 and num_weeks < 6:
            num_weeks += 1
        return num_weeks

    def _select_exercises(self):
        """
        Shuffles the names of all exercises

        Returns:
            A list of exercises names that are shuffled
        """
        exercise_list = list(self._exercises.keys())
        random.shuffle(exercise_list)
        return exercise_list


    @transaction.atomic
    def generate_workout_plan(self, person, preferred_days):
        """
        This method generates a workout plan for a given person and their preferred workout days. 
        It calculates the person's BMI and determines the sets and reps based on their gender and BMI. 
        It determines the number of weeks for the workout plan based on the number of preferred days and the year. 
        It selects exercises that haven't been used yet and creates a new WorkoutPlan object for the person. 
        It loops through each week in the workout plan and creates a new Week object for each week. 
        It loops through each preferred day in the person's list of preferred days and creates a new Day object for each day. 
        It selects an exercise that hasn't been used more than twice on previous days and creates a new Exercise object for the current exercise. 
        If the exercise is time-based, it checks if it has a time limit or not and creates the Exercise object with its attributes. 
        Finally, it bulk creates the ExerciseSteps objects of the exercise. 

        Args:
            person (Person): A Person object representing the person for whom the workout plan is being generated.
            preferred_days (list of str): A list of strings representing the preferred workout days of the person.

        Returns:
            bool: True if the workout plan is successfully generated, False otherwise.

        """
        if not person:
            return "Person is missing"

        if not preferred_days:
            return "Preferred days list is missing"
        
        # Calculate person's BMI
        bmi = self._calculate_bmi(person)

        # Determine sets and reps based on person's gender and BMI
        sets, reps = self._determine_sets_and_reps(person, bmi)
        if not sets:
            return "Sets could not be determined"
        
        if not reps:
            return "Reps could not be determined"
        
        # Determine number of weeks for the workout plan based on the number of preferred days and the year
        num_weeks = self._determine_num_weeks(preferred_days)
        if not num_weeks:
            return "Number of weeks could not be determined"
            
        # Select a list of exercises that haven't been used yet
        exercise_list = self._select_exercises()


        # Create a new WorkoutPlan object for the person

        # gets their most recent workout plan
        try:
            latest_workout_plan = WorkoutPlan.objects.filter(person=person).latest()
            workout_plan = WorkoutPlan.objects.create(
                person=person,
                name=f"{len(preferred_days)}/{num_weeks} CHALLENGE",
                number=latest_workout_plan.number + 1)
            
        except ObjectDoesNotExist:
            workout_plan = WorkoutPlan.objects.create(
                person=person,
                name=f"{len(preferred_days)}/{num_weeks} CHALLENGE",
                number=1)

        if not workout_plan:
            return "Failed to create a Workout Object"
            
        first_week_object_created = False

        # Loop through each week in the workout plan
        for week in range(1, num_weeks + 1):

            if not first_week_object_created:
                week_object = Week.objects.create(workout_plan=workout_plan, number=week, current_week=True)
                if not week_object:
                    return "Failed to create a week object"
                else:
                    first_week_object_created = True
            else:
                week_object = Week.objects.create(workout_plan=workout_plan, number=week)
            
            # Loop through each preferred day in the person's list of preferred days
            for day in range(1, len(preferred_days) + 1):

                # Determine the number of exercises for the current day
                current_day_exercises_count = random.randint(4, 6)
                day_name = preferred_days[day - 1]

                # Create a new Day object for the current day
                day_object = Day.objects.create(week=week_object, number=self.__days_of_the_week.index(day_name) + 1, name=day_name)

                # Keep track of the exercises that have been selected for the current day
                day_exercises = []
                
                # Loop through each exercise for the current day
                for i in range(current_day_exercises_count):

                    # If there are no more exercises left to choose from, select exercises that haven't been used yet
                    if not exercise_list:
                        exercise_list = self._select_exercises()
                    
                    exercise = exercise_list.pop()
                    day_exercises.append(exercise)

                    # Create a new Exercise object for the current exercise
                    if self._exercises.get(exercise):

                        exercise_data = self._exercises[exercise]

                        # Check if the exercise is time based
                        is_time_based = exercise_data.get("time", False)

                        # Check if the exercise has a time limit
                        no_time_limit = exercise_data.get("no_time_limit", False)

                        # Create the Exercise object with its attributes
                        if is_time_based:
                            if no_time_limit:
                                exercise_object = Exercise.objects.create(
                                        day=day_object, 
                                        name=exercise, 
                                        description=exercise_data["description"], 
                                        time_based=True, 
                                        time=None, 
                                        no_time_limit=True,
                                        link=exercise_data["link"])
                            else:
                                exercise_object = Exercise.objects.create(
                                    day=day_object, 
                                    name=exercise, 
                                    description=exercise_data["description"], 
                                    time_based=True, 
                                    time=exercise_data["duration"], 
                                    no_time_limit=False,
                                    link=exercise_data["link"])
                        else:
                            exercise_object = Exercise.objects.create(
                                day=day_object, 
                                name=exercise, 
                                description=exercise_data["description"], 
                                reps=reps, 
                                sets=sets,
                                link=exercise_data["link"]
                            )
                        
                        # Bulk create the ExerciseSteps objects of the exercise
                        exercise_steps = [ExerciseSteps(exercise=exercise_object, instruction=step) for step in exercise_data["steps"].values()]
                        ExerciseSteps.objects.bulk_create(exercise_steps)
        return True

