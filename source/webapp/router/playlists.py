

from pathlib import Path
import urllib.parse


from flask import redirect, render_template, request, Blueprint
from flask_login import current_user, login_required
import requests


import database
import spotify
from spotify.classes import Playlist
from trinkgo.classes import PlaylistSet


WEBAPP_DIRECTORY = Path(__file__).parents[1]
HTML_DIRECTORY = WEBAPP_DIRECTORY / "html"
STATIC_DIRECTORY = WEBAPP_DIRECTORY / "static"


playlists_blueprint = Blueprint('playlists_blueprint', __name__, template_folder=HTML_DIRECTORY, static_folder=STATIC_DIRECTORY)


@playlists_blueprint.get("/playlists")
@playlists_blueprint.get("/playlists/")
def GET_playlists():
	playlists = database.playlists.select_playlists()
	return render_template("playlists/index.j2", playlists=playlists)


@playlists_blueprint.get("/playlists/new")
@login_required
def GET_playlists_new():
	return render_template("playlists/new.j2")


@playlists_blueprint.post("/playlists/new")
@login_required
def POST_playlists_new():
	playlist_link = request.form.get("playlist_link-input")
	path = Path(urllib.parse.urlparse(playlist_link).path)

	playlist = spotify.requests.data.get_playlist(current_user, path.name)
	database.playlists.insert_playlist(playlist)

	return redirect(f"/playlists/{playlist.id}")


@playlists_blueprint.get("/playlists/<int:id>")
@login_required
def GET_playlists_playlist(id: int):
	playlist: Playlist = database.playlists.select_playlist(id)
	database.songs.select_songs_for_playlist(playlist)
	playlist_sets: list[PlaylistSet] = database.playlist_sets.select_playlist_sets()

	return render_template("playlists/playlist/index.j2", playlist=playlist, playlist_sets=playlist_sets)


@playlists_blueprint.get("/playlists/<int:id>/songs")
@login_required
def GET_playlists_playlist_songs(id: int):
	playlist: Playlist = database.playlists.select_playlist(id)
	playlist_sets: list[PlaylistSet] = database.playlist_sets.select_playlist_sets()

	return render_template("playlists/playlist/songs.j2", playlist=playlist)


# ——————————————— SETS ——————————————— #
# TODO: Move to submodule

@playlists_blueprint.get("/playlists/<int:id>/sets")
@login_required
def GET_playlists_playlist_sets(id: int):
	playlist: Playlist = database.playlists.select_playlist(id)
	playlist_sets: list[PlaylistSet] = database.playlist_sets.select_playlist_sets()

	return render_template("playlists/playlist/sets/index.j2", playlist=playlist, playlist_sets=playlist_sets)


@playlists_blueprint.get("/playlists/<int:id>/sets/new")
@login_required
def GET_playlists_playlist_sets_new(id: int):
	playlist = database.playlists.select_playlist(id)

	return render_template("playlists/playlist/sets/new.j2", playlist=playlist)


@playlists_blueprint.post("/playlists/<int:id>/sets/new")
@login_required
def POST_playlists_playlist_sets_new(id: int):
	set_name = request.form.get("set_name-input")

	playlist = database.playlists.select_playlist(id)
	playlist_set = PlaylistSet(id=0, name=set_name, playlist=playlist, set_songs=[])

	database.playlist_sets.insert_set(playlist_set)

	return redirect(f"/playlists/{id}/sets/{playlist_set.id}")


@playlists_blueprint.get("/playlists/<int:playlist_id>/sets/<int:playlist_set_id>")
@login_required
def GET_playlists_playlist_sets_set(playlist_id: int, playlist_set_id: int):
	playlist_set = database.playlist_sets.select_playlist_set(playlist_set_id)
	database.set_songs.select_set_songs_for_playlist_set(playlist_set)

	return render_template("playlists/playlist/sets/set.j2", playlist_set=playlist_set)
