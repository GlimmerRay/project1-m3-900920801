# import flask
# from flask_login.utils import login_required
# import os
import flask
from flask import request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    current_user,
    login_required,
)
from flask_cors import CORS, cross_origin

from spotify_stuff import get_track, artistid_isvalid
from genius_stuff import get_song_url
from fix_db_url import fix_db_url

import os
import requests
import random

import json

app = flask.Flask(__name__, static_folder="./build/static")
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type' 
# This tells our Flask app to look at the results of `npm build` instead of the
# actual files in /templates when we're looking for the index page file. This allows
# us to load React code into a webpage. Look up create-react-app for more reading on
# why this is necessary.
bp = flask.Blueprint("bp", __name__, template_folder="./build")


def create_the_db_object():
    database_url = os.environ["DATABASE_URL"]  # get the location of the database
    database_url = fix_db_url(database_url)  # fix the database_url to avoid an error
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = database_url  # tell flask where to find the database
    app.config[
        "SQLALCHEMY_TRACK_MODIFICATIONS"
    ] = False  # Add this line to fix a warning
    db = SQLAlchemy(app)  # initialize the database object
    return db


def enable_cookies():
    app.secret_key = bytes(
        os.environ["FLASK_SECRET_KEY"], "utf-8"
    )  # Necessary to use cookies (which flask login uses)


def create_the_login_manager():
    login_manager = LoginManager()
    login_manager.init_app(app)
    return login_manager


db = create_the_db_object()
enable_cookies()
login_manager = create_the_login_manager()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    artist_ids = db.Column(db.ARRAY(db.String(64)), nullable=True)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    # flask login's load_user() will receive the return value of this function
    def get_id(self):
        return self.username

    def __repr__(self):
        return "<User %r>" % self.username


# flask login passes the value from get_id() in the User model
# to load_user(), and you should tell it how to use that value
# to load a user. Since I programmed the User model to return
# the username from get_id(), I can assume that this function
# is receiving a username.
@login_manager.user_loader
def load_user(username):
    return User.query.filter_by(username=username).first()

class DBHelpers:

    @classmethod
    def printAllUsers(cls):
        print(User.query.all())
    
    @classmethod
    def getUser(cls, username):
        return User.query.filter_by(username=username).first()

    @classmethod
    def addNewUser(cls, name):
        _user = User(username=name, artist_ids=[])
        db.session.add(_user)
        db.session.commit()
    
    @classmethod
    def getArtistIds(cls, username):
        return DBHelpers.getUser(username).artist_ids
    
    @classmethod
    def removeAllData(cls):
        db.drop_all()
    
    # this should be updated to make sure duplicate ids can't be added
    @classmethod
    def addArtistId(cls, username, artist_id): 
        user = DBHelpers.getUser(username)
        _ids = list(user.artist_ids)
        _ids.append(artist_id)
        user.artist_ids = _ids
        db.session.commit()


@bp.route("/index")
# @login_required
def index():
    # TODO: insert the data fetched by your app main page here as a JSON
    DATA = {"your": "data here"}
    data = json.dumps(DATA)
    return flask.render_template(
        "index.html",
        data=data,
    )


app.register_blueprint(bp)

@app.route("/signup", methods=["POST"])
def signup_post():
    data = json.loads(request.data)
    username = data['username']
    user = User.query.filter_by(username=username).first()
    if user != None:
        return json.dumps({'username_taken': True})
    else:
        DBHelpers.addNewUser(username)
        print(User.query.all())
        return json.dumps({'username_taken': False})


@app.route("/login", methods=["POST"])
def login():
    print('attempting to log in')
    data = json.loads(request.data)
    username = data['username']
    user = User.query.filter_by(username=username).first()
    if user != None:
        login_user(user)

        return json.dumps({'login_successful': True, 'username': current_user.username})

    else:
        return json.dumps({'login_successful': False})


# @app.route("/login", methods=["POST"])
# def login_post():
#     ...


@app.route("/save", methods=["GET"])
def save():
    print('XXXXXXXXXXXXXX')
    return json.dumps(['xxx'])


@app.route("/")
def main():
    ...


app.run(
    host=os.getenv("IP", "0.0.0.0"),
    port=int(os.getenv("PORT", 8081)),
)
