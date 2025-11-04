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


from flask import render_template, Blueprint
from flask_login import login_required


home_blueprint = Blueprint('home_blueprint', __name__)


@home_blueprint.get("/")
@home_blueprint.get("/home")
@login_required
def GET_home():
	return render_template("index.j2")


@home_blueprint.get("/player")
@login_required
def GET_play():
	return render_template("play.j2")
