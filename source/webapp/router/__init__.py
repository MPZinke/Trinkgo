#!/opt/homebrew/bin/python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2025.06.04                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


import base64
from pathlib import Path
import random
import string
import urllib.parse


from flask import redirect, render_template, request, Flask
import requests


import database
import spotify
from spotify.classes import Player, Playlist, Song


WEBAPP_DIRECTORY = Path(__file__).parents[1]
HTML_DIRECTORY = WEBAPP_DIRECTORY / "html"
STATIC_DIRECTORY = WEBAPP_DIRECTORY / "static"


PLAYER = Player()


app = Flask("Catan", template_folder=HTML_DIRECTORY, static_folder=STATIC_DIRECTORY)


def authorize(function: callable) -> callable:
	def wrapper(*args: list, **kwargs: dict):
		if(PLAYER.expired):
			if(PLAYER.refresh_token is None):
				return redirect("/login")

			try:
				spotify.requests.refresh_access_token(PLAYER)

			except requests.exceptions.HTTPError:
				return redirect("/login")

		return function(*args, **kwargs)

	wrapper.__name__ = function.__name__
	wrapper.__annotations__ = function.__annotations__

	return wrapper


@app.route("/login")
def login():
	# FROM: https://developer.spotify.com/documentation/web-playback-sdk/howtos/web-app-player
	#    @: Request User Authorization
	params = {
		"response_type": "code",
		"client_id": "8dc7f8b757934d9ebaf39f9347bccc56",
		"scope": "user-modify-playback-state app-remote-control streaming user-top-read user-read-email user-read-private",
		"state": "",
		"redirect_uri": "http://127.0.0.1:8080/authenticated",
	}
	param_string = urllib.parse.urlencode(params)

	return redirect(f"https://accounts.spotify.com/authorize?{param_string}")


@app.route("/authenticated")
def authenticated():
	code = request.args.get("code")
	if(code is None):
		raise Exception("URL parameter `code` is missing.")

	spotify.requests.get_access_token(PLAYER, code)


	return redirect("/home")


@app.get("/")
@app.get("/home")
@authorize
def GET_home():
	return render_template("home.j2", access_token=PLAYER.access_token)


@app.get("/playlists")
def GET_playlists():
	...


@app.get("/playlists/new")
@authorize
def GET_playlists_new():
	return render_template("playlists/new.j2")


@app.post("/playlists/new")
@authorize
def POST_playlists_new():
	playlist_link = request.form.get("playlist_link-input")
	path = Path(urllib.parse.urlparse(playlist_link).path)

	playlist = spotify.requests.get_playlist(PLAYER, path.name)
	database.playlist.insert_playlist(playlist)

	return redirect(f"/playlists/{path.name}")


@app.get("/playlists/<string:id>")
# @authorize
def GET_playlists_id(id: int):
	playlist = database.playlist.select_playlist(id)

	return render_template("playlists/playlist.j2", playlist=playlist)



@app.post("/api/device_id")
def POST_device_id():
	PLAYER.device_id = request.json.get("device_id")
	return ("", 204)


@app.get("/api/play")
def api_play():
	# song = Song("7zLGHdfJ3JRPxvc96mEPEi", "Out Of Touch", 0)
	# spotify.requests.play_song(PLAYER, song)
	playlist = Playlist("49PAThhKRCCTXeydvq9uAp", "80's Stuff", [])
	spotify.requests.play_playlist(PLAYER, playlist)
	return ("", 204)


@app.get("/api/next")
def api_next():
	spotify.requests.play_next(PLAYER)
	return ("", 204)


@app.get("/api/pause")
def api_pause():
	spotify.requests.pause(PLAYER)
	return ("", 204)
