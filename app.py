"""Runs webpage backend"""
import os
import json
import flask
from flask_login import (
    LoginManager,
    login_manager,
    login_required,
    login_user,
    logout_user,
    current_user,
)
from sqlalchemy import exc

from app_setup import app
from utilities.models import db, Account, FavArtists
import utilities.api_funcs as apf
import utilities.util_funcs as uf

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

bp = flask.Blueprint("bp", __name__, template_folder="./build")


@bp.route("/index")
@login_required
def flask_main():
    """Main flask page."""
    artists = FavArtists.query.filter_by(user=current_user.username).all()
    if len(artists) > 0:
        artist = artists[uf.get_random_num(0, len(artists) - 1)]
        artist = artist.artist_id
        track_artist = apf.get_artist_name(artist)
        (
            track_album_link,
            track_name,
            track_album,
            track_preview,
            backup_link,
            release_year,
            genius_link,
        ) = apf.request_artist_top_track(artist)
        artists_saved = apf.check_artists_saved(current_user.username)
        is_artists_saved = apf.check_if_artists_saved(current_user.username)
    else:
        artist = None
        track_artist = None
        track_album_link = None
        track_name = None
        track_album = None
        track_preview = None
        backup_link = None
        release_year = None
        genius_link = None
        artists_saved = None
        is_artists_saved = False

    data = {
        "track_album_link": track_album_link,
        "track_artist": track_artist,
        "track_name": track_name,
        "track_album": track_album,
        "track_preview": track_preview,
        "backup_link": backup_link,
        "release_year": release_year,
        "genius_link": genius_link,
        "current_user": current_user.username,
        "are_artists_saved": is_artists_saved,
        "artists_saved": artists_saved,
    }
    data = json.dumps(data)
    return flask.render_template(
        "index.html",
        data=data,
    )


app.register_blueprint(bp)


@login_manager.user_loader
def load_user(user_id):
    """Loads user"""
    return Account.query.get(int(user_id))


@app.route("/login", methods=["GET"])
def login():
    """Log in page"""
    return flask.render_template("splash.html")


@app.route("/login", methods=["POST"])
def login_post():
    """Log in action, if error happens, returns to splash page"""
    user = flask.request.form.get("user")
    if flask.request.form["field"] == "Log-in":
        user = Account.query.filter_by(username=user).first()
        if user:
            login_user(user)
            return flask.redirect(flask.url_for("bp.flask_main"))
        flask.flash("No user known by that name")
    elif flask.request.form["field"] == "Sign-up":
        user = Account(username=user)
        try:
            db.session.add(user)
            db.session.commit()
        except exc.IntegrityError:
            flask.flash(
                "User already exists, please log-in or use a different username."
            )
    return flask.redirect(flask.url_for("login"))

@app.route("/logout", methods=["POST"])
def logout():
    """Logs out a user"""
    logout_user()
    return flask.redirect(flask.url_for("login"))

@app.route("/save", methods=["POST"])
def save():
    """Saves list of changes sent from JS frontend"""
    artist_changes = flask.request.json.get("artist_changes")
    methods = flask.request.json.get("methods")
    warnings = []
    successes = []
    added_id = []
    added_name = []
    for index, method in enumerate(methods):
        if method == "add":
            artist_id = artist_changes[index]
            if apf.is_artist_valid(artist_id):
                exists = FavArtists.query.filter_by(
                    user=current_user.username, artist_id=artist_id
                ).all()
                if len(exists) > 0:
                    warnings.append(f"{artist_id} is already a favorite!")
                    continue
                artist_name = apf.add_fav_artist(current_user.username, artist_id)
                added_name.append(artist_name)
                added_id.append(artist_id)
                successes.append(
                    f"{artist_name}: {artist_id} successfully added to favorites!"
                )
            else:
                warnings.append(f"{artist_id} is not a valid artist ID.")
                continue
        elif method == "delete":
            artist_id = artist_changes[index]
            artist_name = apf.delete_fav_artist(current_user.username, artist_id)
            successes.append(
                f"{artist_name}: {artist_id} successfully removed from favorites!"
            )
    return flask.jsonify(
        {
            "warnings": warnings,
            "successes": successes,
            "added_ids": added_id,
            "added_names": added_name,
        }
    )


@app.route("/")
def main():
    """Checks if user is authenticated, redirects accordingly"""
    if current_user.is_authenticated:
        return flask.redirect(flask.url_for("bp.flask_main"))
    return flask.redirect(flask.url_for("login"))


app.run(
    host=os.getenv("IP", "0.0.0.0"),
    debug=True,
    port=int(os.getenv("PORT", 8081)),
)
