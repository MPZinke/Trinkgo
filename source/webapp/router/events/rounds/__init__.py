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
from trinkgo.create_card import create_cards
from webapp.router import app
from webapp.router.auth import authorize
from webapp.router.events.rounds.cards import cards_blueprint
from webapp.router.events.rounds.play import play_blueprint


WEBAPP_DIRECTORY = Path(__file__).parents[3]
HTML_DIRECTORY = WEBAPP_DIRECTORY / "html"
STATIC_DIRECTORY = WEBAPP_DIRECTORY / "static"


rounds_blueprint = Blueprint('rounds_blueprint', __name__, template_folder=HTML_DIRECTORY, static_folder=STATIC_DIRECTORY)
rounds_blueprint.register_blueprint(cards_blueprint)
rounds_blueprint.register_blueprint(play_blueprint)


@rounds_blueprint.get("/events/<int:id>/rounds")
def GET_events_event_rounds(id: int):
	event: Event = database.event.select_event(id)
	database.round.select_rounds_for_event(event)
	database.playlist_set.select_playlist_sets_for_rounds(event.rounds)

	return render_template("events/event/rounds/index.j2", event=event)


@rounds_blueprint.get("/events/<int:id>/rounds/new")
def GET_events_event_rounds_new(id: int):
	event: Event = database.event.select_event(id)
	playlist_sets: list[PlaylistSet] = database.playlist_set.select_playlist_sets()

	return render_template("events/event/rounds/new.j2", event=event, playlist_sets=playlist_sets)


@rounds_blueprint.post("/events/<int:id>/rounds/new")
def POST_events_event_rounds_new(id: int):
	playlist_set_id = int(request.form.get("playlist_set-select"))
	size_rows = int(request.form.get("round_size_rows-input"))
	size_columns = int(request.form.get("round_size_columns-input"))
	number_of_cards = int(request.form.get("number_of_cards-input"))

	name = request.form.get("round_name-input")
	size = [size_rows, size_columns]

	round = Round(
		id=0,
		name=name,
		size=size,
		start=None,
		ended=False,
		cards=[],
		event=Event(id=id,name=None,date=None,start=None,ended=None,rounds=None),
		played_set_songs=None,
		playlist_set=PlaylistSet(id=playlist_set_id, name=None, playlist=None, set_songs=None),
	)

	database.round.insert_round(round)
	create_cards(round, number_of_cards)

	return redirect(f"/events/{id}/rounds/{round.id}")


@rounds_blueprint.get("/events/<int:event_id>/rounds/<int:round_id>")
def GET_events_event_rounds_round(event_id: int, round_id: int):
	round: Round = database.round.select_round(round_id)
	database.event.select_event_for_round(round)
	database.playlist_set.select_playlist_set_for_round(round)
	database.card.select_cards_for_round(round)

	return render_template("events/event/rounds/round/index.j2", round=round)
