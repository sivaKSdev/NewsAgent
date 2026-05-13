# 🚀 Deployment Guide: Vercel + Flask News Agent

## Prerequisites

- Vercel account (free): https://vercel.com
- GitHub account with your code pushed
- Node.js installed locally (for Vercel CLI)

## ⚠️ Important: Database Considerations

SQLite **doesn't work well** on Vercel's serverless platform. You have 3 options:

### Option 1: PostgreSQL (Recommended for Production)

- Most reliable for serverless
- Works perfectly with Flask-SQLAlchemy
- Free tier available on Render, Railway, or Supabase

### Option 2: MongoDB (Alternative)

- Document database that works with serverless
- Free tier available

### Option 3: SQLite (Only for Testing)

- Won't persist data between deployments
- Use only for testing/demo

---

## Step 1: Set Up PostgreSQL (Recommended)

### A. Using Supabase (Free)

1. Go to https://supabase.com
2. Sign up and create a new project
3. Go to **Settings > Database** and note your connection string
4. Copy your database URL in format: `postgresql://user:password@host:port/database`

### B. Using Railway (Alternative)

1. Go to https://railway.app
2. Sign up with GitHub
3. Create a new PostgreSQL database
4. Copy the database URL

---

## Step 2: Update Your Project

### A. Update `config.py` for Production

```python
import os
from datetime import timedelta

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'

    # Database - Use PostgreSQL for production
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if DATABASE_URL and DATABASE_URL.startswith('postgresql://'):
        # Convert postgres:// to postgresql://
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

    SQLALCHEMY_DATABASE_URI = DATABASE_URL or 'sqlite:///news_app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    # News API configuration
    NEWS_API_KEY = os.environ.get('NEWS_API_KEY') or 'demo'
    NEWS_REFRESH_INTERVAL = 3600

    # Flask-Login configuration
    REMEMBER_COOKIE_DURATION = timedelta(days=7)
```

### B. Install PostgreSQL Driver

Update `requirements.txt`:

```
psycopg2-binary==2.9.7
```

---

## Step 3: Prepare GitHub Repository

### A. Initialize Git (if not already done)

```bash
cd path/to/Claude_project1
git init
git add .
git commit -m "Initial commit: News Agent website"
```

### B. Create GitHub Repository

1. Go to https://github.com/new
2. Create a new repository (e.g., `news-agent`)
3. Don't initialize with README, .gitignore, or license
4. Push your code:

```bash
git remote add origin https://github.com/YOUR_USERNAME/news-agent.git
git branch -M main
git push -u origin main
```

---

## Step 4: Deploy to Vercel

### Option A: Using Vercel Web Interface (Easiest)

1. Go to https://vercel.com
2. Click **"New Project"**
3. Click **"Import Git Repository"**
4. Select your GitHub repository
5. Configure project:
   - **Framework**: Other
   - **Root Directory**: ./
6. Click **"Environment Variables"** and add:

```
SECRET_KEY=your-secret-key-here
DATABASE_URL=your-postgresql-url
NEWS_API_KEY=your-newsapi-key
FLASK_ENV=production
```

7. Click **"Deploy"**

### Option B: Using Vercel CLI (Advanced)

1. Install Vercel CLI:

```bash
npm install -g vercel
```

2. Login to Vercel:

```bash
vercel login
```

3. Deploy:

```bash
vercel
```

4. Follow prompts and select your project settings

5. Add environment variables:

```bash
vercel env add SECRET_KEY
vercel env add DATABASE_URL
vercel env add NEWS_API_KEY
```

---

## Step 5: Configure Environment Variables

In Vercel Dashboard:

1. Go to your project
2. Click **Settings** → **Environment Variables**
3. Add these variables:

| Variable       | Value                                                                |
| -------------- | -------------------------------------------------------------------- |
| `SECRET_KEY`   | Generate: `python -c "import secrets; print(secrets.token_hex(32))"` |
| `DATABASE_URL` | Your PostgreSQL connection URL                                       |
| `NEWS_API_KEY` | Get from https://newsapi.org (free tier)                             |
| `FLASK_ENV`    | `production`                                                         |
| `FLASK_DEBUG`  | `False`                                                              |

---

## Step 6: Initialize Database on Vercel

After your first deployment, initialize the database:

### Option A: Using Vercel Shell (if supported)

```bash
vercel shell
python
>>> from app import app, db
>>> with app.app_context():
>>>     db.create_all()
```

### Option B: Add Initialization Route (Temporary)

Add this to `app.py`:

```python
@app.route('/admin/init-db', methods=['POST'])
def admin_init_db():
    """Initialize database (remove after first use)"""
    if os.environ.get('FLASK_ENV') == 'production':
        return 'Unauthorized', 403

    with app.app_context():
        db.create_all()
    return 'Database initialized', 200
```

Then call: `https://your-app.vercel.app/admin/init-db` (POST request)

---

## Step 7: Test Your Deployment

1. Visit your Vercel deployment URL
2. Create a test account
3. Log in and test the news feed
4. Try saving articles
5. Search for news

---

## 🐛 Troubleshooting

### Issue: "Database connection failed"

- **Solution**: Verify DATABASE_URL in environment variables
- Check PostgreSQL credentials
- Ensure IP whitelisting if required

### Issue: "Module not found" or "No module named 'app'"

- **Solution**: Ensure `vercel.json` is correct
- Check that all files are committed to GitHub
- Verify `requirements.txt` has all dependencies

### Issue: "Static files not loading"

- **Solution**: Flask serves templates automatically with Vercel
- Check CSS and JS are in `templates/` folder
- Verify `render_template()` paths

### Issue: "502 Bad Gateway"

- **Solution**: Check Vercel logs: Dashboard → Deployments → Logs
- Verify environment variables are set
- Ensure database is accessible

---

## 📊 View Deployment Logs

```bash
vercel logs
```

Or in Vercel Dashboard:

- Go to **Deployments** → Select latest → View **Logs**

---

## 🔄 Update Your Deployment

After making changes:

```bash
git add .
git commit -m "Description of changes"
git push origin main
```

Vercel will automatically redeploy!

---

## 💾 Database Backups

For PostgreSQL databases:

**Supabase**: Dashboard → Settings → Backups
**Railway**: Dashboard → PostgreSQL → Backups

---

## 🔒 Security Checklist

- ✅ Set `SECRET_KEY` to a random value
- ✅ Use `SESSION_COOKIE_SECURE = True`
- ✅ Use `SESSION_COOKIE_HTTPONLY = True`
- ✅ Never commit `.env` files
- ✅ Use environment variables for sensitive data
- ✅ Enable HTTPS (automatic on Vercel)
- ✅ Keep dependencies updated

---

## 📈 Scaling & Optimization

### Enable Caching

```python
# In app.py
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/dashboard')
@cache.cached(timeout=300)
def dashboard():
    # Cached for 5 minutes
    pass
```

### Use CDN for Static Files

- Configure Vercel to serve static files from global CDN
- Already done by default!

### Database Indexing

```python
# In models.py
class User(UserMixin, db.Model):
    username = db.Column(db.String(80), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
```

---

## 🚀 Custom Domain

1. Buy domain from registrar (GoDaddy, Namecheap, etc.)
2. In Vercel: **Settings** → **Domains**
3. Add your domain
4. Update DNS records (instructions provided by Vercel)
5. Wait for DNS propagation (usually 24-48 hours)

---

## 📞 Support

- Vercel Docs: https://vercel.com/docs
- Flask Docs: https://flask.palletsprojects.com
- GitHub Issues: Create issue in your repo

---

**Your Flask News Agent is now deployed to the cloud! 🎉**
