import logging
import tweepy
import hashlib
from apscheduler.schedulers.background import BackgroundScheduler
from tenacity import retry, stop_after_attempt, wait_exponential
from database import get_sync_session, SentTweet
from config import Config
import time

logger = logging.getLogger(__name__)

class TwitterClient:
    def __init__(self):
        self.auth = tweepy.OAuth1UserHandler(
            Config.TWITTER_API_KEY,
            Config.TWITTER_API_SECRET,
            Config.TWITTER_ACCESS_TOKEN,
            Config.TWITTER_ACCESS_TOKEN_SECRET
        )
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, max=60))
    def send_tweet(self, tweet_text: str):
        """Send tweet with duplicate check"""
        with get_sync_session() as session:
            # Check duplicates
            if session.query(SentTweet).filter(SentTweet.tweet == tweet_text).first():
                logger.warning(f"Duplicate tweet prevented: {tweet_text[:30]}...")
                return

            # Send tweet
            self.api.update_status(tweet_text)
            
            # Log in DB
            session.add(SentTweet(tweet=tweet_text))
            session.commit()
            logger.info(f"Tweet sent: {tweet_text[:30]}...")

def tweet_scheduler():
    """Schedule tweet posting"""
    Config.validate()
    client = TwitterClient()
    scheduler = BackgroundScheduler()
    
    def job():
        try:
            with get_sync_session() as session:
                # Get available tweets
                candidates = [t for t in Config.TWEETS if t]
                sent = {t.tweet for t in session.query(SentTweet.tweet).all()}
                candidates = [t for t in candidates if t not in sent]
                
                if candidates:
                    selected = random.choice(candidates)
                    client.send_tweet(selected)
                
        except Exception as e:
            logger.error(f"Scheduler error: {str(e)}")

    scheduler.add_job(job, 'interval', hours=2)
    scheduler.start()
    
    try:
        while True:
            time.sleep(3600)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

if __name__ == '__main__':
    tweet_scheduler()