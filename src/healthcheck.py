import asyncio
import logging
from database import database_health_check

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

async def startup_checks():
    """Perform system startup checks"""
    logger.info("Starting system health checks...")
    
    max_retries = 5
    for attempt in range(1, max_retries + 1):
        if await database_health_check():
            logger.info("✅ Database connection established")
            return
        logger.warning(f"⚠️ Database connection failed (attempt {attempt}/{max_retries})")
        await asyncio.sleep(5)
    
    raise RuntimeError("Failed to connect to database after multiple attempts")

if __name__ == "__main__":
    asyncio.run(startup_checks())