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


from pathlib import Path


from flask import render_template, Blueprint
from flask_login import current_user, login_required
import requests


from trinkgo import database
from trinkgo import spotify


WEBAPP_DIRECTORY = Path(__file__).parents[1]
HTML_DIRECTORY = WEBAPP_DIRECTORY / "html"
STATIC_DIRECTORY = WEBAPP_DIRECTORY / "static"


home_blueprint = Blueprint('home_blueprint', __name__, template_folder=HTML_DIRECTORY, static_folder=STATIC_DIRECTORY)


@home_blueprint.get("/")
@home_blueprint.get("/home")
@login_required
def GET_home():
	return render_template("index.j2")


@home_blueprint.get("/player")
@login_required
def GET_play():
	return render_template("play.j2")
