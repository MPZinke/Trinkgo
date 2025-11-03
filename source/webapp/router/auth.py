#!/opt/homebrew/bin/python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2025.09.25                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


from datetime import datetime, timedelta
import json
from pathlib import Path
import urllib.parse


from flask import redirect, render_template, request, Blueprint
import flask_login
from flask_login import login_required
import requests


import database
from webapp.router import app
import spotify
from spotify.auth import SpotifyUserAuth


WEBAPP_DIRECTORY = Path(__file__).parents[1]
HTML_DIRECTORY = WEBAPP_DIRECTORY / "html"
STATIC_DIRECTORY = WEBAPP_DIRECTORY / "static"


auth_blueprint = Blueprint('auth_blueprint', __name__, template_folder=HTML_DIRECTORY, static_folder=STATIC_DIRECTORY)


REDIRECT = None  # TODO: Move to session


login_manager = flask_login.LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(auth_json: str):
	auth_dict: dict = json.loads(auth_json)
	return SpotifyUserAuth(
		access_token=auth_dict["access_token"],
		code=auth_dict["code"],
		expiration=datetime.strptime(auth_dict["expiration"], "%Y-%m-%d %H:%M:%S.%f"),
		refresh_token=auth_dict["refresh_token"],
	)


@login_manager.unauthorized_handler
def unauthorized():
	return redirect("/login")


@auth_blueprint.get('/login')
def GET_login():
	return render_template("login.j2")


@auth_blueprint.post('/login')
def POST_login():
	backdoor_username: str = "trinkgo"
	backdoor_password: str = "!!!BorisIstDerBeste!!!"
	username: str = request.form.get("username-input")
	password: str = request.form.get("password-input")

	if(username.lower() != backdoor_username or password != backdoor_password):
		return render_template("login.j2", unauthorized=True)

	params = {
		"response_type": "code",
		"client_id": "8dc7f8b757934d9ebaf39f9347bccc56",
		"scope": "user-modify-playback-state app-remote-control streaming user-top-read user-read-email user-read-private",
		"state": "",
		"redirect_uri": "http://127.0.0.1:8080/authenticated",
	}
	param_string = urllib.parse.urlencode(params)

	return redirect(f"https://accounts.spotify.com/authorize?{param_string}")


@auth_blueprint.get("/authenticated")
def authenticated():
	code = request.args.get("code")
	if(code is None):
		raise Exception("URL parameter `code` is missing.")

	auth_data: dict = spotify.requests.auth.get_access_token(code)
	user = SpotifyUserAuth(
		access_token=auth_data["access_token"],
		code=code,
		expiration=datetime.now() + timedelta(seconds=auth_data["expires_in"]),
		refresh_token=auth_data["refresh_token"],
	)

	flask_login.login_user(user)

	return redirect("/home")


@auth_blueprint.get("/logout")
@login_required
def logout():
	flask_login.logout_user()
	return redirect("/")




# ————————————————————————————————————————————————————— SPOTIFY  ————————————————————————————————————————————————————— #

@auth_blueprint.get("/spotify/login")
def GET_spotify_login():
	# FROM: https://developer.spotify.com/documentation/web-playback-sdk/howtos/web-app-player
	#    @: Request User Authorization
	global REDIRECT

	REDIRECT = request.args.get("post_login_redirect")

	params = {
		"response_type": "code",
		"client_id": "8dc7f8b757934d9ebaf39f9347bccc56",
		"scope": "user-modify-playback-state app-remote-control streaming user-top-read user-read-email user-read-private",
		"state": "",
		"redirect_uri": "http://127.0.0.1:8080/spotify/authenticated",
	}
	param_string = urllib.parse.urlencode(params)

	return redirect(f"https://accounts.spotify.com/authorize?{param_string}")


@auth_blueprint.route("/spotify/authenticated")
def GET_spotify_authenticated():
	global REDIRECT

	code = request.args.get("code")
	if(code is None):
		raise Exception("URL parameter `code` is missing.")

	app.tokens.code = code

	if(REDIRECT is not None):
		post_login_redirect = REDIRECT
		REDIRECT = None
		return redirect(post_login_redirect)

	return redirect("/home")
