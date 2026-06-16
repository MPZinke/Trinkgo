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
import os
import random
import string
import urllib.parse


from flask import redirect, render_template, request, session, Blueprint
import flask_login
from flask_login import login_required
import requests


from trinkgo import spotify
from trinkgo.spotify.auth import SpotifyUserAuth


auth_blueprint = Blueprint('auth_blueprint', __name__)


login_manager = flask_login.LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"


PROTOCOL = os.getenv("PROTOCOL", "https")


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
	session["redirect"] = request.full_path
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

	url = urllib.parse.urlparse(request.url)
	params = {
		"response_type": "code",
		"client_id": os.environ["CLIENT_ID"],
		"scope": "user-modify-playback-state app-remote-control streaming user-top-read user-read-email user-read-private",
		"state": "".join(random.choices(string.ascii_letters + string.digits, k=16)),
		"redirect_uri": f"""{PROTOCOL}://{url.netloc}/authenticated""",
	}
	param_string = urllib.parse.urlencode(params)

	return redirect(f"https://accounts.spotify.com/authorize?{param_string}")


@auth_blueprint.get("/authenticated")
def authenticated():
	code = request.args.get("code")
	if(code is None):
		raise Exception("URL parameter `code` is missing.")

	url = urllib.parse.urlparse(request.url)
	auth_data: dict = spotify.requests.auth.get_access_token(code, f"{PROTOCOL}://{url.netloc}")
	user = SpotifyUserAuth(
		access_token=auth_data["access_token"],
		code=code,
		expiration=datetime.now() + timedelta(seconds=auth_data["expires_in"]),
		refresh_token=auth_data["refresh_token"],
	)
	flask_login.login_user(user)

	if("redirect" in session):
		return redirect(session.pop("redirect"))

	return redirect("/home")


@auth_blueprint.get("/logout")
@login_required
def logout():
	flask_login.logout_user()
	return redirect("/")
