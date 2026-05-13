# 🚀 Complete Vercel Deployment Guide

This guide walks you through deploying the Flask News Agent application to Vercel with PostgreSQL database.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Step 1: Database Setup (PostgreSQL)](#step-1-database-setup-postgresql)
3. [Step 2: GitHub Repository Setup](#step-2-github-repository-setup)
4. [Step 3: Vercel Deployment](#step-3-vercel-deployment)
5. [Step 4: Environment Variables](#step-4-environment-variables)
6. [Step 5: Database Initialization](#step-5-database-initialization)
7. [Testing & Troubleshooting](#testing--troubleshooting)

---

## Prerequisites

Before starting, you need:

- ✅ **Vercel Account** (free at https://vercel.com)
- ✅ **GitHub Account** (free at https://github.com)
- ✅ **PostgreSQL Database** (see Step 1)
- ✅ **NewsAPI Key** (free at https://newsapi.org)
- ✅ **Local Git Setup**

### Recommended: Install Git

If you don't have Git, download from https://git-scm.com/download/win

---

## Step 1: Database Setup (PostgreSQL)

### Option A: Using Supabase (Recommended - Easiest)

1. Go to https://supabase.com and sign up (free tier available)
2. Click "New Project"
3. Fill in:
   - Project name: `news-app` (or your preference)
   - Password: Generate a strong password (save it!)
   - Region: Select closest to you
4. Wait for project to initialize (2-3 minutes)
5. Once ready, go to **Settings > Database**
6. Copy the **Connection string** (PostgreSQL format) - it looks like:
   ```
   postgresql://postgres:[PASSWORD]@[HOST]:5432/postgres
   ```
7. **Save this connection string** - you'll need it in Step 4

### Option B: Using Railway

1. Go to https://railway.app and sign up
2. Click "Create New Project" → "Deploy from GitHub" (or "Provision PostgreSQL")
3. Select PostgreSQL
4. Wait for database to initialize
5. Click the PostgreSQL service, go to **Data** tab
6. Copy the connection URL from the right panel
7. **Save this connection string** - you'll need it in Step 4

---

## Step 2: GitHub Repository Setup

### 2.1 Initialize Local Git Repository

Open PowerShell in your project folder and run:

```powershell
cd "c:\Users\siva1\Documents\Python Scripts\Claude_project1"
git init
git add .
git commit -m "Initial commit: Flask News Agent Application"
```

### 2.2 Create GitHub Repository

1. Go to https://github.com/new
2. Name: `news-agent` (or your preference)
3. Add description: "Flask News Agent with authentication and PostgreSQL"
4. Choose **Public** (required for free Vercel deployment)
5. **Do NOT** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"
7. You'll see instructions - copy the **HTTPS URL** (looks like: `https://github.com/YOUR-USERNAME/news-agent.git`)

### 2.3 Push to GitHub

In PowerShell, run:

```powershell
git remote add origin https://github.com/YOUR-USERNAME/news-agent.git
git branch -M main
git push -u origin main
```

Replace `YOUR-USERNAME` with your actual GitHub username.

**Expected output:**

```
Enumerating objects: XX, done.
Counting objects: 100% (XX/XX), done.
Compressing objects...
...
* [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

---

## Step 3: Vercel Deployment

### 3.1 Connect Vercel to GitHub

1. Go to https://vercel.com/dashboard
2. Click "New Project"
3. Click "Import from Git"
4. Connect your GitHub account (authorize if prompted)
5. Find and select your `news-agent` repository
6. Click "Import"

### 3.2 Configure Project Settings

You should see the import dialog. Before deploying:

1. **Root Directory**: Leave as `.`
2. **Framework Preset**: Select "Other" (since it's Flask)
3. **Build Command**: Leave empty (Vercel will auto-detect)
4. **Output Directory**: Leave empty
5. Click "Deploy"

Vercel will now build and deploy your app (this takes 1-3 minutes).

---

## Step 4: Environment Variables

After the initial deployment attempt (which will fail without env vars), you need to set environment variables.

### 4.1 Get Your Secret Key

In PowerShell, run:

```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output - this is your SECRET_KEY.

### 4.2 Set Variables in Vercel

1. Go to your Vercel project dashboard
2. Go to **Settings > Environment Variables**
3. Add these variables (click "Add" for each):

| Variable       | Value                        | Example                                        |
| -------------- | ---------------------------- | ---------------------------------------------- |
| `FLASK_ENV`    | `production`                 | `production`                                   |
| `SECRET_KEY`   | Your generated key           | `a1b2c3d4e5f6...`                              |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://postgres:pwd@host:5432/postgres` |
| `NEWS_API_KEY` | From newsapi.org             | `your_api_key_here`                            |

**Important**:

- Paste your PostgreSQL connection string exactly as you copied it
- Replace `[PASSWORD]` in connection strings if needed
- Get NEWS_API_KEY from https://newsapi.org (free tier works)

### 4.3 Redeploy with Environment Variables

1. In Vercel dashboard, go to **Deployments**
2. Click the latest failed deployment
3. Click "Redeploy" (or use top menu: **Deployments > Redeploy**)
4. Select "Yes, redeploy"

Vercel will rebuild with the new environment variables. This should succeed now (1-3 minutes).

---

## Step 5: Database Initialization

After successful Vercel deployment, you need to initialize the database tables.

### 5.1 Check Your Vercel App URL

1. In Vercel dashboard, look for your app's URL (it's shown at the top)
2. It looks like: `https://news-agent-abc123.vercel.app`

### 5.2 Initialize Database

You can initialize the database in several ways:

**Option A: Using Vercel CLI (Recommended)**

1. Install Vercel CLI:

   ```powershell
   npm install -g vercel
   ```

2. Link your local project to Vercel:

   ```powershell
   cd "c:\Users\siva1\Documents\Python Scripts\Claude_project1"
   vercel link
   ```

3. Pull production environment:

   ```powershell
   vercel env pull .env.production.local
   ```

4. Create a database initialization script (`init_db_prod.py`):

   ```python
   import os
   from app import app, db

   # Load production environment
   from dotenv import load_dotenv
   load_dotenv('.env.production.local')

   with app.app_context():
       db.create_all()
       print("✓ Database initialized successfully!")
   ```

5. Run it:
   ```powershell
   python init_db_prod.py
   ```

**Option B: Manual Database Initialization**

1. Visit your Vercel app URL: `https://your-app-name.vercel.app/`
2. Try to register a new user
3. This will trigger database table creation
4. If it fails, check Vercel logs (in dashboard, view function logs)

---

## Testing & Troubleshooting

### 5.1 Test the Deployment

1. Visit your app URL: `https://your-app-name.vercel.app`
2. You should see the login page
3. Click "Register" and create a test account
4. Log in with your account
5. You should see news articles on the dashboard

### 5.2 Common Issues

**Issue 1: "502 Bad Gateway"**

- Cause: Usually missing environment variables
- Fix: Check Vercel Settings > Environment Variables, verify all 4 variables are set

**Issue 2: "Database Connection Error"**

- Cause: DATABASE_URL not set or incorrect
- Fix:
  1. Verify PostgreSQL connection string in Vercel env vars
  2. Check database is running (try connecting locally)
  3. Ensure firewall allows connections

**Issue 3: "ModuleNotFoundError"**

- Cause: Missing Python dependencies
- Fix:
  1. Check requirements.txt is in root folder
  2. All dependencies listed there
  3. Redeploy from Vercel dashboard

**Issue 4: "Error at runtime: max() takes 1 positional argument (2 given)"**

- Cause: Jinja2 template issues
- Fix: Already fixed in app.py (app.jinja_env.globals.update)

### 5.3 View Logs

In Vercel dashboard:

1. Go to **Deployments**
2. Click the latest deployment
3. Click **Runtime logs** tab
4. View full error messages here

---

## Production Optimization

### 6.1 Custom Domain (Optional)

In Vercel dashboard:

1. Go to **Settings > Domains**
2. Click "Add Domain"
3. Enter your domain (e.g., `mynewsapp.com`)
4. Follow DNS setup instructions from your domain registrar

### 6.2 Enable Analytics

In Vercel dashboard:

1. Go to **Settings > Analytics**
2. Enable to see traffic and performance metrics

### 6.3 Set Up Deployments

Every time you push to GitHub, Vercel auto-deploys:

```powershell
# Make local changes
git add .
git commit -m "Update news categories"
git push origin main
# Vercel automatically redeploys!
```

---

## Security Checklist

Before going live:

- ✅ SECRET_KEY is changed and strong (32+ chars)
- ✅ DATABASE_URL is PostgreSQL (not SQLite)
- ✅ FLASK_ENV is set to "production"
- ✅ SESSION_COOKIE_SECURE is enabled
- ✅ NewsAPI key is valid
- ✅ Repository is Public (for free Vercel)
- ✅ No `.env` file committed to git
- ✅ Database backups enabled (if using Supabase/Railway)

---

## Monitoring & Support

### Monitor Your App

1. **Vercel Dashboard**: Check deployments, logs, analytics
2. **NewsAPI**: Monitor API usage at https://newsapi.org/account
3. **Database**: Check PostgreSQL storage usage

### Get Help

- Vercel Docs: https://vercel.com/docs
- Flask Docs: https://flask.palletsprojects.com
- PostgreSQL: https://www.postgresql.org/docs
- NewsAPI Issues: https://newsapi.org/support

---

## Next Steps

After successful deployment:

1. ✅ Test all features (registration, login, news, search, save articles)
2. ✅ Share your app URL with friends: `https://your-app-name.vercel.app`
3. ✅ Add a custom domain if desired
4. ✅ Set up continuous monitoring
5. ✅ Plan future enhancements (email notifications, social sharing, etc.)

---

**Congratulations! 🎉 Your Flask News Agent is now live on Vercel!**
