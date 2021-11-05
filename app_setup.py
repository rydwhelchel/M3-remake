from logging import logThreads
import os
import flask
from dotenv import load_dotenv
from dotenv.main import find_dotenv

load_dotenv(find_dotenv())

app = flask.Flask(__name__, static_folder="./build/static")
app.secret_key = os.urandom(24)

url = os.getenv("DATABASE_URL")
if url.startswith("postgres://"):
    url = url.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
