# Production WSGI entry point for Vercel
from app import app

# Vercel requires the app variable to be available
if __name__ == '__main__':
    app.run()
