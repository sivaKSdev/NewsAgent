from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from config import Config
from models import db, User, SavedNews
from news_agent import NewsAgent
from datetime import datetime
import os

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

# Initialize news agent
news_agent = NewsAgent(api_key=app.config['NEWS_API_KEY'])

# Make built-in functions available to Jinja2 templates
app.jinja_env.globals.update(max=max, min=min)


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login"""
    return User.query.get(int(user_id))


@app.before_request
def before_request():
    """Update last login time on every request"""
    if current_user.is_authenticated:
        current_user.last_login = datetime.utcnow()
        db.session.commit()


@app.route('/')
def index():
    """Home page - redirects to dashboard if logged in"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')

        # Validation
        if not username or not email or not password:
            flash('All fields are required.', 'error')
            return redirect(url_for('register'))

        if password != password_confirm:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('register'))

        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
            return redirect(url_for('register'))

        # Check if user exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'error')
            return redirect(url_for('register'))

        if User.query.filter_by(email=email).first():
            flash('Email already exists.', 'error')
            return redirect(url_for('register'))

        # Create new user
        try:
            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()

            flash(f'Account created successfully! You can now log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration.', 'error')
            app.logger.error(f"Registration error: {e}")
            return redirect(url_for('register'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('Username and password are required.', 'error')
            return redirect(url_for('login'))

        user = User.query.filter_by(username=username).first()

        if user is None or not user.check_password(password):
            flash('Invalid username or password.', 'error')
            return redirect(url_for('login'))

        if not user.is_active:
            flash('Your account has been disabled.', 'error')
            return redirect(url_for('login'))

        login_user(user, remember=request.form.get('remember_me'))
        flash(f'Welcome back, {user.username}!', 'success')

        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('dashboard'))

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    """Logout user"""
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard showing latest news"""
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', None)

    # Fetch news
    news = news_agent.fetch_top_headlines(category=category)

    # Paginate (10 per page)
    per_page = 10
    total_news = news
    start = (page - 1) * per_page
    end = start + per_page
    paginated_news = total_news[start:end]

    total_pages = (len(total_news) + per_page - 1) // per_page

    return render_template(
        'dashboard.html',
        news=paginated_news,
        page=page,
        total_pages=total_pages,
        category=category
    )


@app.route('/search', methods=['GET'])
@login_required
def search():
    """Search for news articles"""
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)

    if not query:
        flash('Please enter a search query.', 'warning')
        return redirect(url_for('dashboard'))

    # Search news
    news = news_agent.search_news(query)

    # Paginate
    per_page = 10
    total_news = news
    start = (page - 1) * per_page
    end = start + per_page
    paginated_news = total_news[start:end]

    total_pages = (len(total_news) + per_page - 1) // per_page

    return render_template(
        'search_results.html',
        news=paginated_news,
        query=query,
        page=page,
        total_pages=total_pages
    )


@app.route('/save-news', methods=['POST'])
@login_required
def save_news():
    """Save a news article"""
    data = request.get_json()

    if not data or not data.get('title') or not data.get('url'):
        return jsonify({'success': False, 'message': 'Invalid data'}), 400

    try:
        # Check if already saved
        existing = SavedNews.query.filter_by(
            user_id=current_user.id,
            url=data.get('url')
        ).first()

        if existing:
            return jsonify({'success': False, 'message': 'News already saved'}), 409

        saved_news = SavedNews(
            user_id=current_user.id,
            title=data.get('title'),
            description=data.get('description', ''),
            url=data.get('url'),
            source=data.get('source', 'Unknown'),
            published_at=data.get('published_at')
        )

        db.session.add(saved_news)
        db.session.commit()

        return jsonify({'success': True, 'message': 'News saved successfully'})

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Save news error: {e}")
        return jsonify({'success': False, 'message': 'Error saving news'}), 500


@app.route('/saved-news')
@login_required
def saved_news():
    """View saved news articles"""
    page = request.args.get('page', 1, type=int)
    per_page = 10

    saved = SavedNews.query.filter_by(user_id=current_user.id)\
        .order_by(SavedNews.saved_at.desc())\
        .paginate(page=page, per_page=per_page)

    return render_template(
        'saved_news.html',
        saved_news=saved.items,
        page=page,
        total_pages=saved.pages,
        total_items=saved.total
    )


@app.route('/delete-saved/<int:news_id>', methods=['POST'])
@login_required
def delete_saved(news_id):
    """Delete a saved news article"""
    saved = SavedNews.query.get(news_id)

    if not saved:
        flash('News article not found.', 'error')
        return redirect(url_for('saved_news'))

    if saved.user_id != current_user.id:
        flash('Unauthorized access.', 'error')
        return redirect(url_for('dashboard'))

    try:
        db.session.delete(saved)
        db.session.commit()
        flash('News article deleted.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting news article.', 'error')
        app.logger.error(f"Delete news error: {e}")

    return redirect(url_for('saved_news'))


@app.route('/api/stats')
@login_required
def api_stats():
    """Get user statistics"""
    saved_count = SavedNews.query.filter_by(user_id=current_user.id).count()

    return jsonify({
        'username': current_user.username,
        'email': current_user.email,
        'saved_news_count': saved_count,
        'created_at': current_user.created_at.isoformat(),
        'last_login': current_user.last_login.isoformat() if current_user.last_login else None
    })


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    db.session.rollback()
    return render_template('500.html'), 500


def init_db():
    """Initialize database with tables"""
    with app.app_context():
        db.create_all()
        print("Database initialized successfully!")


if __name__ == '__main__':
    # Initialize database
    init_db()

    # Run Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
