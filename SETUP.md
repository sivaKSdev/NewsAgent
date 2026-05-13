# 🚀 Quick Start Guide

## 1️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

## 2️⃣ Run the Application

```bash
python app.py
```

## 3️⃣ Access the Website

Open your browser and go to:

```
http://localhost:5000
```

## 4️⃣ Create an Account

1. Click "Register"
2. Enter username, email, and password
3. Click "Register"
4. Log in with your credentials

## 5️⃣ Explore News

- Browse latest news on the dashboard
- Filter by category (Business, Technology, etc.)
- Search for specific topics
- Save articles to your collection
- Visit saved articles anytime

## 📌 Important Notes

- **First Run**: The database (`news_app.db`) will be created automatically
- **No API Key Needed**: Demo articles display if NewsAPI isn't configured
- **Real News**: Get a free API key from [newsapi.org](https://newsapi.org) and add it to `.env`
- **Port**: Default is 5000. To change, edit `app.py` last line

## 🔧 For Real News

1. Visit https://newsapi.org
2. Sign up for a free account
3. Get your API key
4. Create `.env` file:
   ```
   NEWS_API_KEY=your-key-here
   ```
5. Restart the app

## 📱 Features

✅ User Authentication (Registration & Login)
✅ SQLite Database for Users & Passwords
✅ News Agent (Fetches Latest News)
✅ Importance Scoring System
✅ Save Articles Feature
✅ Search Functionality
✅ Category Filtering
✅ Responsive Design
✅ Session Management

Enjoy! 📰
