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
from typing import Optional
import urllib.parse


from flask import redirect, render_template, request, Flask
import requests


import database
import spotify
from spotify.auth import Tokens
from spotify.classes import Playlist, Song


WEBAPP_DIRECTORY = Path(__file__).parents[1]
HTML_DIRECTORY = WEBAPP_DIRECTORY / "html"
STATIC_DIRECTORY = WEBAPP_DIRECTORY / "static"


app = Flask("Trinkgo", template_folder=HTML_DIRECTORY, static_folder=STATIC_DIRECTORY)
app.tokens = Tokens()
app.context_processor(app.tokens.context_processor)


@app.get("/favicon.ico")
def favicon():
	return ("", 204)
