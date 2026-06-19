from SQLite.connection import get_database_path
from flask import Flask
from Flask.routes import init_routes 
from dotenv import load_dotenv



import os

app = Flask(__name__)

DATABASE_PATH = get_database_path()
load_dotenv()
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
init_routes(app)

if __name__ == "__main__":
    app.run(debug=True)