

import os
from pathlib import Path
from typing import Optional
import urllib.parse


from flask import redirect, render_template, request, Blueprint
import requests


import database
import spotify
from spotify.auth import TOKENS
from webapp.router.auth import authorize
from spotify.classes import Playlist, Song
from trinkgo.classes import PlaylistSet, SetSong


WEBAPP_DIRECTORY = Path(__file__).parents[1]
HTML_DIRECTORY = WEBAPP_DIRECTORY / "html"
STATIC_DIRECTORY = WEBAPP_DIRECTORY / "static"


playlists_blueprint = Blueprint('playlists_blueprint', __name__, template_folder=HTML_DIRECTORY, static_folder=STATIC_DIRECTORY)


@playlists_blueprint.get("/playlists")
@playlists_blueprint.get("/playlists/")
def GET_playlists():
	playlists = database.playlist.select_playlists()
	return render_template("playlists/index.j2", playlists=playlists)


@playlists_blueprint.get("/playlists/new")
@authorize
def GET_playlists_new():
	return render_template("playlists/new.j2")


@playlists_blueprint.post("/playlists/new")
@authorize
def POST_playlists_new():
	playlist_link = request.form.get("playlist_link-input")
	path = Path(urllib.parse.urlparse(playlist_link).path)

	playlist = spotify.requests.data.get_playlist(TOKENS, path.name)
	database.playlist.insert_playlist(playlist)

	return redirect(f"/playlists/{playlist.id}")


@playlists_blueprint.get("/playlists/<int:id>")
@authorize
def GET_playlists_id(id: int):
	playlist = database.playlist.select_playlist(id)
	playlist_sets = database.playlist_set.select_playlist_sets()

	return render_template("playlists/playlist.j2", playlist=playlist, playlist_sets=playlist_sets, access_token=TOKENS.access_token)


@playlists_blueprint.post("/playlists/<int:id>")
@authorize
def POST_playlists_id(id: int):
	playlist = database.playlist.select_playlist(id)
	number_of_boards = request.form.get("number_of_boards-input")

	return redirect(f"/playlists/{id}")


@playlists_blueprint.get("/playlists/<int:id>/sets/new")
@authorize
def GET_playlists_id_sets_new(id: int):
	playlist = database.playlist.select_playlist(id)

	return render_template("playlists/sets/new.j2")


@playlists_blueprint.post("/playlists/<int:id>/sets/new")
@authorize
def POST_playlists_id_sets_new(id: int):
	set_name = request.form.get("set_name-input")

	playlist = database.playlist.select_playlist(id)
	playlist_set = PlaylistSet(id=0, name=set_name, playlist=playlist, songs=[])

	database.playlist_set.insert_set(playlist_set)

	return render_template("playlists/sets/set.j2")


@playlists_blueprint.get("/playlists/<int:playlist_id>/sets/<int:playlist_set_id>")
@authorize
def GET_playlists_id_sets_set(playlist_id: int, playlist_set_id: int):
	playlist_set = database.playlist_set.select_playlist_set(playlist_set_id)

	return render_template("playlists/sets/set.j2", playlist_set=playlist_set)
