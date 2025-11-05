#!/opt/homebrew/bin/python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2025.11.04                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


from pathlib import Path
import urllib.parse


from flask import redirect, render_template, request, Blueprint
from flask_login import current_user, login_required
import requests


from trinkgo import database
from trinkgo import spotify
from trinkgo.spotify.classes import Playlist
from trinkgo.game.classes import PlaylistSet
from trinkgo.webapp.router.playlists.sets import playlist_sets_blueprint


playlists_blueprint = Blueprint('playlists_blueprint', __name__)
playlists_blueprint.register_blueprint(playlist_sets_blueprint)


@playlists_blueprint.get("/playlists")
@playlists_blueprint.get("/playlists/")
@login_required
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

	return render_template("playlists/playlist/songs.j2", playlist=playlist)
