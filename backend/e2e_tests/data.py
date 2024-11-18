from backend.domains.activities.schemas import Activity, Unit, ScoreType

activities = [
    Activity(
        id=1,
        name="Bench press",
        description="5 x 135# bench press",
        weight=135,
        reps=5,
        time=None,
        unit=Unit.LB,
        score_type=ScoreType.WEIGHT
    ),
    Activity(
        id=2,
        name="Squat",
        description="5 x 225# squat",
        weight=225,
        reps=5,
        time=None,
        unit=Unit.LB,
        score_type=ScoreType.WEIGHT
    ),
    Activity(
        id=3,
        name="Deadlift",
        description="5 x 315# deadlift",
        weight=315,
        reps=5,
        time=None,
        unit=Unit.LB,
        score_type=ScoreType.WEIGHT
    )
]