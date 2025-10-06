#!/opt/homebrew/bin/python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2025.10.05                                                                                                      #
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
from typing import Optional
import urllib.parse


from flask import redirect, render_template, request, Flask, Blueprint
import requests


import database
import spotify
from spotify.auth import Tokens
from spotify.classes import Playlist, Song
from webapp.router.auth import authorize


WEBAPP_DIRECTORY = Path(__file__).parents[1]
HTML_DIRECTORY = WEBAPP_DIRECTORY / "html"
STATIC_DIRECTORY = WEBAPP_DIRECTORY / "static"


home_blueprint = Blueprint('home_blueprint', __name__, template_folder=HTML_DIRECTORY, static_folder=STATIC_DIRECTORY)


@home_blueprint.get("/")
@home_blueprint.get("/home")
@authorize
def GET_home():
	return render_template("index.j2")


@home_blueprint.get("/player")
@authorize
def GET_play():
	return render_template("play.j2")
