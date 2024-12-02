from datetime import date
from backend.domains.activities.schemas import CreateActivityRequest, ScoreType
from backend.domains.scores.schemas import CreateScoreRequest
from backend.client.client import Client
from backend.domains.users.schemas import CreateUserRequest


def get_or_create_user(client: Client, name: str, email: str):
    try:
        user = client.get_user(name)
    except Exception as e:
        user = client.add_user(CreateUserRequest(name=name, email=email))
    return user


def create_workout(client: Client):
    # Base workout metadata
    workout_date = date(2024, 11, 10)
    workout_name = "Guy's Workout - 11/10/24"
    workout_description = "A full-body workout with warmups, track laps, and circuits."

    # Fetch the user ID for "guy"
    user = get_or_create_user(client, "guy", "guysayfan@gmail.com")
    user_id = user.id

    # Create the main workout activity
    workout_request = CreateActivityRequest(
        name=workout_name,
        description=workout_description,
        score_type=ScoreType.FIXED.value,  # The workout itself doesn't have a varying score
        sub_activities=[]
    )
    workout_activity = client.add_activity(workout_request)

    # Define activities and scores
    activities = []
    scores = []

    # Helper function to create an activity and its score
    def add_activity_and_score(name, description, score_type, notes):
        activity_request = CreateActivityRequest(
            name=name,
            description=description,
            score_type=score_type
        )
        activity = client.add_activity(activity_request)
        activities.append(activity)

        score_request = CreateScoreRequest(
            user_id=user_id,
            activity_id=activity.id,
            when=str(workout_date),
            notes=notes
        )
        score = client.add_score(score_request)
        scores.append(score)
        return activity

    # Track laps
    track_activity = add_activity_and_score(
        name="4 Laps Around Track",
        description="Running 4 laps around the track.",
        score_type=ScoreType.FIXED.value,
        notes="Completed 4 laps."
    )

    # Warmup bench press
    warmup_bench_activity = add_activity_and_score(
        name="Bench Press Warmup",
        description="1 set of 15 reps with 95 lbs.",
        score_type=ScoreType.FIXED.value,
        notes="1x15; 95 lbs."
    )

    # Main bench press
    bench_press_activity = add_activity_and_score(
        name="Bench Press",
        description="4 sets of 5 reps with 135 lbs.",
        score_type=ScoreType.FIXED.value,
        notes="4x5; 135 lbs."
    )

    # Circuit activities
    circuit_activities = [
        {
            "name": "Strict Press",
            "description": "3 sets of 5 reps with 95 lbs.",
            "score_type": ScoreType.FIXED.value,
            "notes": "3x5; 95 lbs."
        },
        {
            "name": "Lunges",
            "description": "3 sets of 12 reps each side.",
            "score_type": ScoreType.FIXED.value,
            "notes": "3x12 (e.s.)."
        },
        {
            "name": "Goblet Squats",
            "description": "3 sets of 15 reps with 48.5 lbs.",
            "score_type": ScoreType.FIXED.value,
            "notes": "3x15; 48.5 lbs."
        },
        {
            "name": "Sit Ups",
            "description": "3 sets of 20 reps.",
            "score_type": ScoreType.FIXED.value,
            "notes": "3x20."
        },
        {
            "name": "Plank",
            "description": "3 sets of 1-minute holds.",
            "score_type": ScoreType.FIXED.value,
            "notes": "3x1min."
        }
    ]

    # Add circuit activities to the workout
    for circuit_activity in circuit_activities:
        activity = add_activity_and_score(
            name=circuit_activity["name"],
            description=circuit_activity["description"],
            score_type=circuit_activity["score_type"],
            notes=circuit_activity["notes"]
        )
        workout_request.sub_activities.append(activity.id)

    # Update the workout with its sub-activities
    workout_activity = client.add_activity(workout_request)

    return workout_activity, activities, scores


# Initialize the client
client = Client(base_url="http://localhost:8000")

# Generate the workout, activities, and scores
workout, activities, scores = create_workout(client)

# Print the results for review
print("Workout:")
print(workout)
print("\nActivities:")
for activity in activities:
    print(activity)
print("\nScores:")
for score in scores:
    print(score)
