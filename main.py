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

from spotify_stuff import get_track, artistid_isvalid
from genius_stuff import get_song_url
from fix_db_url import fix_db_url

import os
import requests
import random


app = flask.Flask(__name__)

def create_the_db_object():
    database_url = os.environ["DATABASE_URL"]  # get the location of the database
    database_url = fix_db_url(database_url)  # fix the database_url to avoid an error
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = database_url  # tell flask where to find the database
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Add this line to fix a warning
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

@app.route("/random-song")
@login_required
def random_song():
    artist_ids = current_user.artist_ids
    if len(artist_ids) == 0:
        return flask.redirect("artistid_form")
    random_id = random.choice(artist_ids)
    preview_url, track_name, artist_name, img_url = get_track(random_id)
    lyrics_url = get_song_url(track_name, artist_name)

    _args = {
        "preview_url": preview_url,
        "track_name": track_name,
        "artist_name": artist_name,
        "img_url": img_url,
        "lyrics_url": get_song_url(track_name, artist_name),
        "current_user": current_user,
    }

    return flask.render_template("random_song.html", args=_args)


@app.route("/artistid_form", methods=["POST", "GET"])
@login_required
def artistid_form():
    if request.method == "POST":
        artist_id = request.form["artist-id"]
        if artistid_isvalid(artist_id):
            username = current_user.username
            DBHelpers.addArtistId(username, artist_id)
        return flask.render_template("artistid_form.html", current_user=current_user)
    return flask.render_template("artistid_form.html", current_user=current_user)


@app.route("/signup_form", methods=["POST", "GET"])
def signup_form():
    if request.method == "POST":
        username = request.form["username"]
        # If the username is already taken we should show an error!!
        if User.query.filter_by(username=username).first() != None:
            flash('username is taken')
            return flask.render_template("signup_form.html")
        else:
            DBHelpers.addNewUser(username)
    return flask.render_template("signup_form.html")


@app.route("/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        user = User.query.filter_by(username=username).first()
        if user != None:
            login_user(user)
            return flask.redirect("/random-song")
        else:
            return flask.render_template("login_form.html", invalid_user=True)
    return flask.render_template("login_form.html", invalid_user=False)

@app.route("/logout")
def logout():
    logout_user()
    return flask.redirect("/")


app.run(host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", 8080)), debug=True)
