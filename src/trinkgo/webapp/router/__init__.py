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
import secrets
import string
from typing import Optional
import urllib.parse


from flask import redirect, render_template, request, Flask
import requests


from trinkgo import database
from trinkgo import spotify
from trinkgo.spotify.classes import Playlist, Song
from trinkgo.webapp.router.api import api_blueprint
from trinkgo.webapp.router.auth import auth_blueprint, login_manager
from trinkgo.webapp.router.events import events_blueprint
from trinkgo.webapp.router.home import home_blueprint
from trinkgo.webapp.router.playlists import playlists_blueprint


WEBAPP_DIRECTORY = Path(__file__).parents[1]
HTML_DIRECTORY = WEBAPP_DIRECTORY / "html"
STATIC_DIRECTORY = WEBAPP_DIRECTORY / "static"


app = Flask("Trinkgo", template_folder=HTML_DIRECTORY, static_folder=STATIC_DIRECTORY)
app.secret_key = secrets.token_hex(64)
login_manager.init_app(app)
app.register_blueprint(api_blueprint)
app.register_blueprint(auth_blueprint)
app.register_blueprint(events_blueprint)
app.register_blueprint(home_blueprint)
app.register_blueprint(playlists_blueprint)


@app.get("/favicon.ico")
def favicon():
	return ("", 204)
