import logging
import os
import time
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import text
from database import get_sync_session
from config import Config
from telegram import Bot

logger = logging.getLogger(__name__)

class DBCleanup:
    @staticmethod
    def maintain():
        """Perform database maintenance tasks"""
        logger.info("Starting database maintenance")
        try:
            with get_sync_session() as session:
                # Clean old records
                session.execute(text("""
                    DELETE FROM workout_history 
                    WHERE timestamp < NOW() - INTERVAL '30 days'
                """))
                
                # Vacuum database
                session.execute(text("VACUUM ANALYZE"))
                session.commit()
                
                # Create backup
                backup_path = DBCleanup.create_backup()
                logger.info(f"Backup created at {backup_path}")
                
                # Send backup to admin
                DBCleanup.send_backup(backup_path)
                
                # Rotate backups
                DBCleanup.rotate_backups()
                
        except Exception as e:
            logger.error(f"Maintenance failed: {str(e)}")

    @staticmethod
    def create_backup() -> str:
        """Create database backup"""
        backup_dir = "/tmp/backups"
        os.makedirs(backup_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        return f"{backup_dir}/backup_{timestamp}.sql"

    @staticmethod
    def send_backup(backup_path: str):
        """Send backup via Telegram"""
        try:
            bot = Bot(token=Config.TELEGRAM_BOT_TOKEN)
            with open(backup_path, "rb") as f:
                bot.send_document(chat_id=Config.ADMIN_CHAT_ID, document=f)
        except Exception as e:
            logger.error(f"Failed to send backup: {str(e)}")

    @staticmethod
    def rotate_backups(days_to_keep: int = 7):
        """Rotate old backups"""
        cutoff = datetime.now() - timedelta(days=days_to_keep)
        backup_dir = "/tmp/backups"
        
        for filename in os.listdir(backup_dir):
            path = os.path.join(backup_dir, filename)
            if os.stat(path).st_mtime < cutoff.timestamp():
                os.remove(path)
                logger.info(f"Deleted old backup: {filename}")

def main():
    """Start cleanup scheduler"""
    scheduler = BackgroundScheduler()
    scheduler.add_job(DBCleanup.maintain, 'interval', days=1)
    scheduler.start()
    
    try:
        while True:
            time.sleep(86400)  # 24 hours
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

if __name__ == '__main__':
    main()