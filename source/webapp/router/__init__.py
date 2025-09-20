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


from pathlib import Path


from flask import redirect, render_template, request, Flask
import requests


WEBAPP_DIRECTORY = Path(__file__).parents[1]
HTML_DIRECTORY = WEBAPP_DIRECTORY / "html"
STATIC_DIRECTORY = WEBAPP_DIRECTORY / "static"

print(HTML_DIRECTORY)

BEARER_TOKEN = None


app = Flask("Catan", template_folder=HTML_DIRECTORY, static_folder=STATIC_DIRECTORY)


@app.route("/authenticate")
def authenticate():
	return render_template("authenticate.j2")



@app.route("/authenticated")
def authenticated():
	global BEARER_TOKEN

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
	BEARER_TOKEN = response.json().get("access_token")
	return redirect("/home")


@app.get("/")
@app.get("/home")
def GET_home():
	if BEARER_TOKEN is None:
		return redirect("/authenticate")

	return render_template("home.j2", bearer_token=BEARER_TOKEN)
