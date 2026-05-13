# 📰 News Agent - Full Stack Python Website

A modern full-stack Python web application that displays the latest news with AI-powered importance scoring. Users must create accounts and log in to view news articles.

## 🎯 Features

- **User Authentication**: Secure registration and login system with password hashing
- **SQLite Database**: Stores user credentials and saved articles
- **News Agent**: Fetches and processes latest news with importance scoring
- **News Categories**: Filter news by category (Business, Technology, Science, Health, Entertainment)
- **Search Functionality**: Search for news articles by keywords
- **Save Articles**: Authenticated users can save articles for later reading
- **Responsive Design**: Beautiful, modern UI that works on desktop and mobile
- **Session Management**: Persistent sessions with "Remember Me" functionality

## 🏗️ Project Structure

```
Claude_project1/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── models.py              # Database models (User, SavedNews)
├── news_agent.py          # News fetching and processing agent
├── requirements.txt       # Python dependencies
├── news_app.db           # SQLite database (created on first run)
└── templates/            # HTML templates
    ├── base.html         # Base template with navigation
    ├── login.html        # Login page
    ├── register.html     # Registration page
    ├── dashboard.html    # Main news feed
    ├── saved_news.html   # Saved articles
    ├── search_results.html # Search results
    ├── 404.html          # 404 error page
    └── 500.html          # 500 error page
```

## 📋 Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

## ⚙️ Installation & Setup

### 1. Clone/Navigate to the project directory

```bash
cd c:\Users\siva1\Documents\Python\ Scripts\Claude_project1
```

### 2. Create a virtual environment (Optional but recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables (Optional)

Create a `.env` file in the project root:

```
SECRET_KEY=your-secret-key-here
NEWS_API_KEY=your-newsapi-key  # Get from https://newsapi.org
```

**Note**: The app works without an API key by using demo articles. For real news, get a free API key from [NewsAPI.org](https://newsapi.org).

### 5. Run the application

```bash
python app.py
```

The application will be available at: `http://localhost:5000`

## 🚀 Usage

### First Time Setup

1. Navigate to `http://localhost:5000`
2. Click "Register" to create a new account
3. Enter username, email, and password (min 6 characters)
4. Log in with your credentials

### Features Overview

**Dashboard**

- View latest news articles
- Filter by category
- See importance scores (0-100%)
- Click "Read Full" to visit the original article
- Click "Save" to save articles for later

**Search**

- Click "Search" button in navigation
- Enter keywords to search news
- Browse search results with pagination

**Saved News**

- View all your saved articles
- Delete articles from your collection
- Access saved articles anytime

## 🗄️ Database

The application uses SQLite with two main tables:

**User Table**

- id (Primary Key)
- username (Unique, Required)
- email (Unique, Required)
- password_hash (Hashed password)
- created_at (Account creation timestamp)
- last_login (Last login timestamp)
- is_active (Account status)

**SavedNews Table**

- id (Primary Key)
- user_id (Foreign Key to User)
- title (Article title)
- description (Article description)
- url (Article URL)
- source (News source)
- published_at (Publication date)
- saved_at (When article was saved)

## 📰 News Agent

The News Agent fetches articles from NewsAPI.org with features:

- **Top Headlines**: Fetches latest headlines from various categories
- **Search**: Search for specific topics
- **Importance Scoring**: Calculates importance based on:
  - Content completeness (description + image)
  - Article recency
  - Custom algorithms
- **Caching**: Caches results for 1 hour to reduce API calls
- **Demo Mode**: Uses demo articles when API is unavailable

## 🔐 Security Features

- Password hashing using Werkzeug
- CSRF protection (built into Flask-WTF compatible forms)
- SQL injection prevention through SQLAlchemy ORM
- Session management with Flask-Login
- Login required decorators on protected routes

## 🎨 Customization

### Change color scheme

Edit the CSS in templates. Main colors are:

- Primary: `#667eea` (Purple)
- Secondary: `#764ba2` (Dark Purple)
- Success: `#28a745` (Green)
- Error: `#dc3545` (Red)

### Change news API

Edit `news_agent.py` to integrate different news sources

### Configure session timeout

Edit `config.py`:

```python
PERMANENT_SESSION_LIFETIME = timedelta(days=7)  # Change to desired duration
```

## 🐛 Troubleshooting

**Port already in use**

```bash
# Change port in app.py: app.run(port=5001)
```

**Database locked**
Delete `news_app.db` and restart:

```bash
del news_app.db
python app.py
```

**API not working**

- Check your internet connection
- Verify NEWS_API_KEY if set
- Demo articles will display if API is unavailable

## 📝 API Endpoints

| Endpoint             | Method    | Description                   |
| -------------------- | --------- | ----------------------------- |
| `/`                  | GET       | Home (redirects to dashboard) |
| `/login`             | GET, POST | User login                    |
| `/register`          | GET, POST | User registration             |
| `/logout`            | GET       | User logout                   |
| `/dashboard`         | GET       | News feed with filters        |
| `/search`            | GET       | Search news                   |
| `/save-news`         | POST      | Save article (AJAX)           |
| `/saved-news`        | GET       | View saved articles           |
| `/delete-saved/<id>` | POST      | Delete saved article          |
| `/api/stats`         | GET       | User statistics (JSON)        |

## 📦 Dependencies

- **Flask** (2.3.3): Web framework
- **Flask-SQLAlchemy** (3.0.5): Database ORM
- **Flask-Login** (0.6.2): User authentication
- **Werkzeug** (2.3.7): Security utilities
- **requests** (2.31.0): HTTP library for news API
- **python-dotenv** (1.0.0): Environment variables

## 🤝 Contributing

Feel free to modify and extend this project for your needs!

## 📄 License

This project is open source and available for educational purposes.

## 🙋 Support

For issues or questions:

1. Check the troubleshooting section
2. Review error logs in the console
3. Ensure all dependencies are installed correctly

---

**Happy News Reading! 📰**
