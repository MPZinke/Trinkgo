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


from pathlib import Path
import urllib.parse


from flask import redirect, request, Blueprint
import requests


import database
from webapp.router import app
import spotify


WEBAPP_DIRECTORY = Path(__file__).parents[1]
HTML_DIRECTORY = WEBAPP_DIRECTORY / "html"
STATIC_DIRECTORY = WEBAPP_DIRECTORY / "static"


auth_blueprint = Blueprint('auth_blueprint', __name__, template_folder=HTML_DIRECTORY, static_folder=STATIC_DIRECTORY)


REDIRECT = None


def authorize(function: callable) -> callable:
	def wrapper(*args: list, **kwargs: dict):
		if(not app.tokens.authenticated):
			param_string = urllib.parse.urlencode({"post_login_redirect": request.full_path})
			return redirect(f"/login?{param_string}")

		return function(*args, **kwargs)

	wrapper.__name__ = function.__name__
	wrapper.__annotations__ = function.__annotations__

	return wrapper


@auth_blueprint.get("/login")
def login():
	# FROM: https://developer.spotify.com/documentation/web-playback-sdk/howtos/web-app-player
	#    @: Request User Authorization
	global REDIRECT

	REDIRECT = request.args.get("post_login_redirect")

	params = {
		"response_type": "code",
		"client_id": "8dc7f8b757934d9ebaf39f9347bccc56",
		"scope": "user-modify-playback-state app-remote-control streaming user-top-read user-read-email user-read-private",
		"state": "",
		"redirect_uri": f"http://127.0.0.1:8080/authenticated",
	}
	param_string = urllib.parse.urlencode(params)

	return redirect(f"https://accounts.spotify.com/authorize?{param_string}")


@auth_blueprint.route("/authenticated")
def authenticated():
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
