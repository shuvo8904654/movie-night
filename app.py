import random
from typing import Dict, Any, Optional

import requests
from flask import Flask, render_template, abort

class AppConfig:
    TMDB_API_KEY = "ec6d0f7af5974ae53b4ec0bae590809a"
    TMDB_BASE_URL = "https://api.themoviedb.org/3"

def create_app() -> Flask:
    flask_app = Flask(__name__)
    flask_app.config.from_object(AppConfig)

    @flask_app.route('/')
    def index():
        return render_template('index.html')
        
    return flask_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
