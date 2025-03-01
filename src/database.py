import logging
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Database setup
Base = declarative_base()

# Async engine for main operations
async_engine = create_async_engine(
    Config.DATABASE_URL,
    pool_size=5,
    max_overflow=2,
    pool_timeout=30,
    pool_recycle=1800,
)

# Sync engine for migrations and maintenance
sync_engine = create_engine(
    Config.DATABASE_URL.replace("+asyncpg", ""),
    pool_pre_ping=True,
)

# Session factories
AsyncSessionLocal = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

SyncSessionLocal = sessionmaker(
    sync_engine,
    expire_on_commit=False,
)

# Models
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    fitness_level = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)

class WorkoutHistory(Base):
    __tablename__ = "workout_history"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    workout = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

class SentTweet(Base):
    __tablename__ = "sent_tweets"
    id = Column(Integer, primary_key=True)
    tweet = Column(Text, unique=True, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Utility functions
async def get_async_session():
    """Provide an async database session"""
    async with AsyncSessionLocal() as session:
        yield session

def get_sync_session():
    """Provide a sync database session"""
    return SyncSessionLocal()

async def database_health_check():
    """Check database connection health"""
    try:
        async with async_engine.connect() as conn:
            await conn.execute("SELECT 1")
        return True
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        return False