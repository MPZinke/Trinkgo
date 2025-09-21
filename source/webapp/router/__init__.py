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


import spotify
from spotify.classes import Player, Song


WEBAPP_DIRECTORY = Path(__file__).parents[1]
HTML_DIRECTORY = WEBAPP_DIRECTORY / "html"
STATIC_DIRECTORY = WEBAPP_DIRECTORY / "static"


PLAYER = Player()


app = Flask("Catan", template_folder=HTML_DIRECTORY, static_folder=STATIC_DIRECTORY)


@app.route("/authenticate")
def authenticate():
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
	# FROM: https://developer.spotify.com/documentation/web-playback-sdk/howtos/web-app-player
	#    @: Request Access Token
	code = request.args.get("code")
	if(code is None):
		raise Exception("URL parameter `code` is missing.")

	url = "https://accounts.spotify.com/api/token"
	headers = {
		"Authorization": "Basic OGRjN2Y4Yjc1NzkzNGQ5ZWJhZjM5ZjkzNDdiY2NjNTY6N2U5YzQyMTI3OWI3NGQ2OWE2YTliNTBlNDkzY2ZhOGU=",
		"Content-Type": "application/x-www-form-urlencoded",
	}
	params = {
		"code": code,
		"grant_type": "authorization_code",
		"redirect_uri": "http://127.0.0.1:8080/authenticated",
	}
	response = requests.post(url, headers=headers, params=params)

	print(response.json())

	PLAYER.access_token = response.json().get("access_token")
	PLAYER.refresh_token = response.json().get("refresh_token")
	return redirect("/home")


@app.get("/")
@app.get("/home")
def GET_home():
	if PLAYER.access_token is None:
		return redirect("/authenticate")

	return render_template("home.j2", access_token=PLAYER.access_token)


@app.post("/api/device_id")
def POST_device_id():
	PLAYER.device_id = request.json.get("device_id")
	return ("", 204)


@app.get("/api/play")
def api_play():
	song = Song("5ChkMS8OtdzJeqyybCc9R5", "Billie Jean", 60_000)
	spotify.requests.play_song(PLAYER, song)
	return ("", 204)


@app.get("/api/pause")
def api_pause():
	spotify.requests.pause(PLAYER)
	return ("", 204)
