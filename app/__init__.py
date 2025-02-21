from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from app.routes import api_bp
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    client = MongoClient(app.config["MONGO_URI"])
    db_name = app.config["USER_DB"]
    app.db = client[db_name]

    app.register_blueprint(api_bp, url_prefix='/api')
    app.url_map.strict_slashes = False

    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)  # Change according to your frontend url
    app.config['CORS_HEADERS'] = 'Content-Type'
    print("in create app")

    return app
