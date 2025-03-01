import random
from config import Config

class WorkoutGenerator:
    @staticmethod
    def generate(fitness_level: int, sport: str) -> tuple[list[str], str]:
        """Generate workout plan based on fitness level and sport"""
        if sport not in Config.ALLOWED_SPORTS:
            raise ValueError(f"Invalid sport. Allowed: {', '.join(Config.ALLOWED_SPORTS)}")
        
        if not 1 <= fitness_level <= 3:
            raise ValueError("Fitness level must be between 1 and 3")

        data = Config.get_workout_data()
        workouts = data["workouts"].get(sport, {})
        plan = workouts.get(str(fitness_level), [])
        
        # Add cooldown exercises
        cooldown = ["Deep Breathing 2min", "Hydration Break", "Static Stretching 5min"]
        full_plan = plan + random.sample(cooldown, 1)
        
        # Get motivation message
        motivation = random.choice(
            [msg for msg in Config.MOTIVATIONAL_MESSAGES if msg]
        )
        
        return full_plan, motivation