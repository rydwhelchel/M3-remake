"""Utilities for accessing Spotify API"""
import os
import base64
import requests
import random

from dotenv import load_dotenv
from dotenv.main import find_dotenv
from .models import db, FavArtists

load_dotenv(find_dotenv())


def add_fav_artist(user, artist_id):
    artist_name = get_artist_name(artist_id=artist_id)
    new_artist = FavArtists(user=user, artist_id=artist_id, artist_name=artist_name)
    db.session.add(new_artist)
    db.session.commit()
    return artist_name


def delete_fav_artist(user, artist_id):
    artist = FavArtists.query.filter_by(user=user, artist_id=artist_id).first()
    db.session.delete(artist)
    artist = artist.artist_name
    db.session.commit()
    return artist


def get_spot_access():
    """Returns the access token from spotify given Key and Secret in .env"""
    ID = os.getenv("SPOT_ID")
    SECRET = os.getenv("SPOT_SECRET")
    POST_URL = "https://accounts.spotify.com/api/token"
    header = {}
    data = {}

    # Creates and encodes the spotify secret
    secret_req = f"{ID}:{SECRET}"
    secret_req = secret_req.encode("ascii")
    secret_req = base64.b64encode(secret_req)
    secret_req = secret_req.decode("ascii")

    data["grant_type"] = "client_credentials"
    header["Authorization"] = f"Basic {secret_req}"

    spot_response = requests.post(POST_URL, headers=header, data=data)

    spot_json = spot_response.json()
    TOKEN = spot_json["access_token"]
    header["Authorization"] = f"Bearer {TOKEN}"
    return header


def get_gen_access():
    """Returns the access token from Genius given Key and Secret in .env"""
    ACCESS_TOKEN = os.getenv("GEN_ACCESS")
    header = {}
    header["Authorization"] = f"Bearer {ACCESS_TOKEN}"
    return header


def request_artist_top_track(artist_id):
    """Requests the json file of the top 10 songs by the artist provided"""
    header = get_spot_access()
    params = {"market": "US"}
    response = requests.get(
        f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks",
        headers=header,
        params=params,
    )
    response_json = response.json()
    track_json = random.choice(response_json["tracks"])
    return get_artist_top_track(track_json)


def get_artist_top_track(response_json):
    """Returns the information about a top track given the index."""
    track_name = response_json["name"]
    track_album = response_json["album"]["name"]
    track_album_link = response_json["album"]["images"][0]["url"]
    track_preview = response_json["preview_url"]
    backup_link = response_json["external_urls"]["spotify"]
    release_date = response_json["album"]["release_date"]
    release_year = release_date[0:4]

    return (
        track_album_link,
        track_name,
        track_album,
        track_preview,
        backup_link,
        release_year,
        get_lyrics(track_name, response_json["artists"][0]["name"]),
    )


def get_lyrics(artist_name, track_name):
    """Searches Genius for lyrics to the track using the Artist's
    name and the name of the track. Top result link is returned."""
    header = get_gen_access()
    query = artist_name + " " + track_name
    params = {
        "q": query,
    }
    response = requests.get(
        "https://api.genius.com/search", headers=header, params=params
    )
    response_json = response.json()
    try:
        genius_link = response_json["response"]["hits"][0]["result"]["url"]
        return genius_link
    except KeyError:
        return "Incorrect key, JSON error."
    except IndexError:
        return "Couldn't fetch song lyrics! There were no results..."


def get_artist_name(artist_id):
    """Returns the name of the artist from the given artist_id"""
    header = get_spot_access()
    response = requests.get(
        f"https://api.spotify.com/v1/artists/{artist_id}", headers=header
    )
    response_json = response.json()
    artist_name = response_json["name"]
    return artist_name


def check_if_artists_saved(user):
    """Checks if there is any artists saved"""
    try:
        artist = FavArtists.query.filter_by(user=user).first()
    except:
        return False
    if artist:
        return True
    else:
        return False


def check_artists_saved(user):
    """Checks if there is any artists saved"""
    artist_dict = {}
    try:
        artists = FavArtists.query.filter_by(user=user).all()
    except:
        return {}
    if len(artists) == 0:
        return {}
    else:
        for artist in artists:
            artist_dict[artist.artist_id] = artist.artist_name
        return artist_dict


def is_artist_valid(artist_id):
    """Checks if the artist_id is valid"""
    header = get_spot_access()
    response = requests.get(
        f"https://api.spotify.com/v1/artists/{artist_id}", headers=header
    )
    response_json = response.json()
    try:
        artist_name = response_json["name"]
    except KeyError:
        return False
    return True


if __name__ == "__main__":
    pass
