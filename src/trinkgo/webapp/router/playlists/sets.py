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


from flask import redirect, render_template, request, Blueprint
from flask_login import login_required
import requests


from trinkgo import database
from trinkgo.game.classes import PlaylistSet
from trinkgo.spotify.classes import Playlist


playlist_sets_blueprint = Blueprint('playlist_sets_blueprint', __name__)


@playlist_sets_blueprint.get("/playlists/<int:id>/sets")
@login_required
def GET_playlists_playlist_sets(id: int):
	playlist: Playlist = database.playlists.select_playlist(id)
	playlist_sets: list[PlaylistSet] = database.playlist_sets.select_playlist_sets()

	return render_template("playlists/playlist/sets/index.j2", playlist=playlist, playlist_sets=playlist_sets)


@playlist_sets_blueprint.get("/playlists/<int:id>/sets/new")
@login_required
def GET_playlists_playlist_sets_new(id: int):
	playlist = database.playlists.select_playlist(id)

	return render_template("playlists/playlist/sets/new.j2", playlist=playlist)


@playlist_sets_blueprint.post("/playlists/<int:id>/sets/new")
@login_required
def POST_playlists_playlist_sets_new(id: int):
	set_name = request.form.get("set_name-input")

	playlist = database.playlists.select_playlist(id)
	playlist_set = PlaylistSet(id=0, name=set_name, playlist=playlist, set_songs=[])

	database.playlist_sets.insert_set(playlist_set)

	return redirect(f"/playlists/{id}/sets/{playlist_set.id}")


@playlist_sets_blueprint.get("/playlists/<int:playlist_id>/sets/<int:playlist_set_id>")
@login_required
def GET_playlists_playlist_sets_set(playlist_id: int, playlist_set_id: int):
	playlist_set = database.playlist_sets.select_playlist_set(playlist_set_id)
	database.set_songs.select_set_songs_for_playlist_set(playlist_set)

	return render_template("playlists/playlist/sets/set.j2", playlist_set=playlist_set)
