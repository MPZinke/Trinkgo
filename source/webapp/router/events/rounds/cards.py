#!/opt/homebrew/bin/python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2025.10.20                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


from datetime import date as date_type
from pathlib import Path


from flask import redirect, render_template, request, Blueprint
import requests


import database
import spotify
from trinkgo.classes import Event, PlaylistSet, Round
from webapp.router import app
from webapp.router.auth import authorize


WEBAPP_DIRECTORY = Path(__file__).parents[3]
HTML_DIRECTORY = WEBAPP_DIRECTORY / "html"
STATIC_DIRECTORY = WEBAPP_DIRECTORY / "static"


cards_blueprint = Blueprint('cards_blueprint', __name__, template_folder=HTML_DIRECTORY, static_folder=STATIC_DIRECTORY)


@cards_blueprint.get("/events/<int:event_id>/rounds/<int:round_id>/cards")
def GET_events_event_rounds_round_cards(event_id: int, round_id: int):
	round: Round = database.round.select_round_all(round_id)

	return render_template("events/event/rounds/round/cards/index.j2", round=round)


@cards_blueprint.post("/events/<int:event_id>/rounds/<int:round_id>/cards/new")
def GET_events_event_rounds_round_cards_new(event_id: int, round_id: int):
	round: Round = database.round.select_round_all(round_id)

	return render_template("events/event/rounds/round/cards/index.j2", round=round)


@cards_blueprint.get("/events/<int:event_id>/rounds/<int:round_id>/cards/<int:card_id>")
def GET_events_event_rounds_round_cards_card(event_id: int, round_id: int, card_id: int):
	# TODO: Display card PDF
	round: Round = database.round.select_round_all(round_id)

	return render_template("events/event/rounds/round/cards/index.j2", round=round)
