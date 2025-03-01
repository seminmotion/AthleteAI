import random
from config import Config

class NutritionPlanner:
    @staticmethod
    def generate(goal: str, fitness_level: int) -> tuple[list[str], str]:
        """Generate nutrition plan based on goal and fitness level"""
        if goal not in Config.ALLOWED_GOALS:
            raise ValueError(f"Invalid goal. Allowed: {', '.join(Config.ALLOWED_GOALS)}")
        
        if not 1 <= fitness_level <= 3:
            raise ValueError("Fitness level must be between 1 and 3")

        data = Config.get_workout_data()
        meals = data["nutrition"].get(goal, {}).get(str(fitness_level), [])
        
        formatted = [f"🍽 {meal} ({random.randint(300,600)}kcal)" for meal in meals]
        motivation = random.choice(
            [msg for msg in Config.MOTIVATIONAL_MESSAGES if msg]
        )
        
        return formatted, motivation