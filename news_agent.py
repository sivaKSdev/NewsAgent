import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any
import time


class NewsAgent:
    """Agent to fetch and process latest news"""

    def __init__(self, api_key: str = 'demo'):
        self.api_key = api_key
        self.base_url = 'https://newsapi.org/v2'
        self.cache = None
        self.cache_time = None
        self.cache_duration = 3600  # 1 hour

    def fetch_top_headlines(self, country: str = 'us', category: str = None) -> List[Dict[str, Any]]:
        """
        Fetch top headlines from NewsAPI

        Args:
            country: Country code (e.g., 'us', 'gb', 'in')
            category: News category (business, entertainment, health, science, sports, technology)

        Returns:
            List of news articles
        """
        # Check cache
        if self.cache and self.cache_time and (time.time() - self.cache_time < self.cache_duration):
            return self.cache

        try:
            params = {
                'apiKey': self.api_key,
                'country': country,
                'pageSize': 20
            }

            if category:
                params['category'] = category

            response = requests.get(
                f'{self.base_url}/top-headlines', params=params, timeout=10)

            if response.status_code == 200:
                articles = response.json().get('articles', [])
                self.cache = self._process_articles(articles)
                self.cache_time = time.time()
                return self.cache
            else:
                print(f"API Error: {response.status_code}")
                return self._get_demo_articles()

        except requests.exceptions.RequestException as e:
            print(f"Network Error: {e}")
            return self._get_demo_articles()

    def search_news(self, query: str, sort_by: str = 'publishedAt') -> List[Dict[str, Any]]:
        """
        Search for news articles by keyword

        Args:
            query: Search query
            sort_by: Sort order (relevancy, popularity, publishedAt)

        Returns:
            List of matching articles
        """
        try:
            params = {
                'apiKey': self.api_key,
                'q': query,
                'sortBy': sort_by,
                'pageSize': 20,
                'language': 'en'
            }

            response = requests.get(
                f'{self.base_url}/everything', params=params, timeout=10)

            if response.status_code == 200:
                articles = response.json().get('articles', [])
                return self._process_articles(articles)
            else:
                return []

        except requests.exceptions.RequestException as e:
            print(f"Network Error: {e}")
            return []

    def _process_articles(self, articles: List[Dict]) -> List[Dict[str, Any]]:
        """
        Process and format articles

        Args:
            articles: Raw articles from API

        Returns:
            Processed articles with summaries
        """
        processed = []
        for article in articles:
            processed_article = {
                'title': article.get('title', 'No title'),
                'description': article.get('description', 'No description'),
                'content': article.get('content', ''),
                'url': article.get('url', ''),
                'image': article.get('urlToImage', ''),
                'source': article.get('source', {}).get('name', 'Unknown'),
                'published_at': article.get('publishedAt', ''),
                'importance': self._calculate_importance(article)
            }
            processed.append(processed_article)

        # Sort by importance
        processed.sort(key=lambda x: x['importance'], reverse=True)
        return processed

    def _calculate_importance(self, article: Dict) -> float:
        """
        Calculate importance score for an article

        Args:
            article: Article data

        Returns:
            Importance score (0-100)
        """
        score = 50  # Base score

        # Increase score if article has all required fields
        if article.get('description') and article.get('urlToImage'):
            score += 20

        # Increase score for recent articles
        try:
            pub_time = datetime.fromisoformat(article.get(
                'publishedAt', '').replace('Z', '+00:00'))
            age_hours = (datetime.now(pub_time.tzinfo) -
                         pub_time).total_seconds() / 3600

            if age_hours < 1:
                score += 20
            elif age_hours < 6:
                score += 10
            elif age_hours < 24:
                score += 5
        except:
            pass

        return min(score, 100)

    def _get_demo_articles(self) -> List[Dict[str, Any]]:
        """
        Get demo articles when API is not available

        Returns:
            List of demo articles
        """
        return [
            {
                'title': 'Python Web Development Guide',
                'description': 'Learn full-stack Python web development with Flask and SQLAlchemy',
                'content': 'Full stack development involves both frontend and backend development...',
                'url': '#',
                'image': 'https://via.placeholder.com/400x200',
                'source': 'Tech News',
                'published_at': datetime.now().isoformat(),
                'importance': 85
            },
            {
                'title': 'Latest AI Trends in 2026',
                'description': 'Discover the emerging trends in artificial intelligence',
                'content': 'AI continues to evolve with new models and applications...',
                'url': '#',
                'image': 'https://via.placeholder.com/400x200',
                'source': 'AI Today',
                'published_at': (datetime.now() - timedelta(hours=2)).isoformat(),
                'importance': 75
            },
            {
                'title': 'Web Security Best Practices',
                'description': 'Essential security measures for modern web applications',
                'content': 'Security is paramount in modern web development...',
                'url': '#',
                'image': 'https://via.placeholder.com/400x200',
                'source': 'Security Weekly',
                'published_at': (datetime.now() - timedelta(hours=4)).isoformat(),
                'importance': 70
            }
        ]
