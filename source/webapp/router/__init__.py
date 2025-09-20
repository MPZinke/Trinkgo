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


from flask import redirect, render_template, Flask


WEBAPP_DIRECTORY = Path(__file__).parents[1]
HTML_DIRECTORY = WEBAPP_DIRECTORY / "html"
STATIC_DIRECTORY = WEBAPP_DIRECTORY / "static"

print(HTML_DIRECTORY)


app = Flask("Catan", template_folder=HTML_DIRECTORY, static_folder=STATIC_DIRECTORY)


@app.route("/authenticate")
def authenticate():
	return render_template("authenticate.j2")



@app.route("/authenticated")
def authenticated():
	return render_template("authenticated.j2")


# @app.route("/callback")
@app.route("/home")
def home():
	return render_template("home.j2")


