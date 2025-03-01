# 🏋️ AthleteAI - Fitness & Motivation

AthleteAI is a Telegram and Twitter AI designed to provide personalized fitness and nutrition plans, user profile tracking, and daily motivation. Whether you're looking for workout guidance, dietary recommendations, or just a boost of inspiration, AthleteAI has you covered!

---

## 🚀 Features

✅ Personalized workout and nutrition plans  
✅ User profile creation and tracking  
✅ Telegram bot interaction  
✅ Automated motivational tweets  
✅ Feedback collection for continuous improvement  

---

## 🛠 Technologies Used

- **Programming Language**: Python
- **Database**: SQLite (AioSQLite for async handling)
- **APIs**: Telegram Bot API, Tweepy (Twitter API)
- **Deployment**: Docker, Railway

---

## 📥 Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/athleteaicoach.git
cd athleteai
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Set Up Environment Variables
Rename `.env.example` to `.env` and update it with your credentials:
```ini
TELEGRAM_BOT_TOKEN=your_bot_token_here
DATABASE_URL=sqlite:///athleteai.db
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
OPENAI_API_KEY=your_openai_key_here
```

### 4️⃣ Run the Bot
```bash
python bot.py
```

---

## 📌 Usage Guide

1. **Start the bot on Telegram**: `/start` to create a user profile.  
2. **Get a workout plan**: `/workout` to receive a personalized workout.  
3. **Receive nutrition tips**: `/nutrition` for dietary advice.  
4. **Check progress**: `/profile` to view and update fitness goals.  
5. **Stay motivated**: Daily motivational messages on Twitter.

---

## 🛠 Deployment (Railway)
1. Create a new project on [Railway.app](https://railway.app/).
2. Set environment variables under the **Variables** section.
3. Deploy using **Railway CLI** or **GitHub integration**.

---

## 🎯 Roadmap

- [ ] Personalized fitness plans
- [ ] Telegram bot functionality
- [ ] Web dashboard for user insights
- [ ] AI-powered workout recommendations

---

## 🤝 Contributing
We welcome contributions! To contribute:
1. **Fork & Clone** the repository
```bash
git clone https://github.com/yourusername/athleteai.git
```
2. **Create a Feature Branch**
```bash
git checkout -b new-feature
```
3. **Commit & Push**
```bash
git commit -m "Add new feature"
git push origin new-feature
```
4. **Submit a Pull Request** 🚀

---

## 📄 License
This project is licensed under the MIT License.

---

## 📬 Contact
For support or collaboration, reach out via [Twitter](https://twitter.com/AthleteAICoach) or [Telegram](https://t.me/AthleteAI_bot).

Happy training! 💪

