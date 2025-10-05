

import os
from pathlib import Path
from typing import Optional
import urllib.parse


from flask import redirect, render_template, request, Blueprint
import requests


import database
import spotify
from spotify.auth import TOKENS
from webapp.router.auth import authorize
from spotify.classes import Playlist, Song


WEBAPP_DIRECTORY = Path(__file__).parents[1]
HTML_DIRECTORY = WEBAPP_DIRECTORY / "html"
STATIC_DIRECTORY = WEBAPP_DIRECTORY / "static"


play_blueprint = Blueprint('play_blueprint', __name__, template_folder=HTML_DIRECTORY, static_folder=STATIC_DIRECTORY)


@play_blueprint.get("/play")
@play_blueprint.get("/play/")
def GET_play():
	play = database.playlist.select_play()
	return render_template("play/index.j2", play=play)


@play_blueprint.get("/play/new")
@play_blueprint.get("/play/new/")
def GET_play():
	play = database.playlist.select_play()
	return render_template("play/index.j2", play=play)

