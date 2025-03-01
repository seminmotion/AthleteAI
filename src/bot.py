import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from sqlalchemy import text
from database import get_async_session
from config import Config
from workout_generator import WorkoutGenerator
from nutrition_plan import NutritionPlanner
from token_bucket import Limiter
import asyncio

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

class FitnessBot:
    def __init__(self):
        self.app = ApplicationBuilder().token(Config.TELEGRAM_BOT_TOKEN).build()
        self.rate_limiter = Limiter(capacity=5, refill_rate=1/60)  # 5 requests/minute
        self._register_handlers()

    def _register_handlers(self):
        """Register all command and message handlers"""
        handlers = [
            CommandHandler("start", self.start),
            CommandHandler("workout", self.workout),
            CommandHandler("nutrition", self.nutrition),
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message),
        ]
        for handler in handlers:
            self.app.add_handler(handler)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        await update.message.reply_text(
            "🏋️ Welcome to FitnessBot!\n\n"
            "Available commands:\n"
            "/workout [sport] - Get personalized workout\n"
            "/nutrition [goal] - Get meal plan"
        )

    async def workout(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /workout command"""
        user = update.effective_user
        if not await self.rate_limiter.consume(f"user:{user.id}"):
            await update.message.reply_text("⚠️ Rate limit exceeded. Try again in 1 minute.")
            return

        try:
            sport = " ".join(context.args).lower() if context.args else "general"
            async with get_async_session() as session:
                # Get or create user
                result = await session.execute(
                    text("SELECT fitness_level FROM users WHERE telegram_id = :id"),
                    {"id": user.id}
                )
                profile = result.fetchone()
                
                if not profile:
                    await session.execute(
                        text("INSERT INTO users (telegram_id) VALUES (:id)"),
                        {"id": user.id}
                    )
                    await session.commit()
                    fitness_level = 1
                else:
                    fitness_level = profile[0]

                # Generate workout
                plan, motivation = WorkoutGenerator.generate(fitness_level, sport)
                
                # Save workout
                await session.execute(
                    text("""
                        INSERT INTO workout_history (user_id, workout)
                        VALUES (
                            (SELECT id FROM users WHERE telegram_id = :id),
                            :workout
                        )
                    """),
                    {"id": user.id, "workout": ", ".join(plan)}
                )
                await session.commit()

                await update.message.reply_text("\n".join(plan))
                await update.message.reply_text(motivation)

        except ValueError as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
        except Exception as e:
            logger.error(f"Workout error: {str(e)}", exc_info=True)
            await update.message.reply_text("⚠️ Failed to generate workout. Try again later.")

    async def nutrition(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /nutrition command"""
        user = update.effective_user
        goal = " ".join(context.args).lower() if context.args else "balance"
        
        try:
            async with get_async_session() as session:
                result = await session.execute(
                    text("SELECT fitness_level FROM users WHERE telegram_id = :id"),
                    {"id": user.id}
                )
                profile = result.fetchone()
                fitness_level = profile[0] if profile else 1
                
                meals, motivation = NutritionPlanner.generate(goal, fitness_level)
                await update.message.reply_text("\n".join(meals))
                await update.message.reply_text(motivation)
                
        except ValueError as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
        except Exception as e:
            logger.error(f"Nutrition error: {str(e)}", exc_info=True)
            await update.message.reply_text("⚠️ Failed to generate nutrition plan")

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle all other messages"""
        await update.message.reply_text(
            "ℹ️ Use commands to interact with me:\n"
            "/workout - Get exercises\n"
            "/nutrition - Get meal plan"
        )

    def run(self):
        """Start the bot"""
        self.app.run_polling()

if __name__ == "__main__":
    Config.validate()
    FitnessBot().run()