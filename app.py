import random
from typing import Dict, Any, Optional

import requests
from flask import Flask, render_template, abort

class AppConfig:
    TMDB_API_KEY = "ec6d0f7af5974ae53b4ec0bae590809a"
    TMDB_BASE_URL = "https://api.themoviedb.org/3"
    MAX_PAGES = 50

class TMDBClient:
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url

    def get_random_movie(self) -> Optional[Dict[str, Any]]:
        page_num = random.randint(1, AppConfig.MAX_PAGES)
        url = f"{self.base_url}/discover/movie"
        
        payload = {
            'api_key': self.api_key,
            'page': page_num,
            'sort_by': 'popularity.desc',
            'include_adult': 'false',
            'include_video': 'false'
        }
        response = requests.get(url, params=payload, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        movies = data.get('results', [])
        if not movies:
            return None
            
        return random.choice(movies)

def create_app() -> Flask:
    flask_app = Flask(__name__)
    flask_app.config.from_object(AppConfig)
    
    tmdb_client = TMDBClient(
        api_key=flask_app.config['TMDB_API_KEY'],
        base_url=flask_app.config['TMDB_BASE_URL']
    )

    @flask_app.route('/')
    def index():
        return render_template('index.html')

    @flask_app.route('/movie')
    def movie():
        try:
            selected_movie = tmdb_client.get_random_movie()
            
            if not selected_movie:
                return abort(500, "Could not find any movies.")
                
            return render_template('movie.html', movie=selected_movie)
            
        except requests.RequestException:
            return abort(500, "Error fetching data from TMDB. Please check your API key and try again.")

    @flask_app.route('/about')
    def about():
        return render_template('about.html')
        
    return flask_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
