#!/opt/homebrew/bin/python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2025.10.11                                                                                                      #
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


WEBAPP_DIRECTORY = Path(__file__).parents[1]
HTML_DIRECTORY = WEBAPP_DIRECTORY / "html"
STATIC_DIRECTORY = WEBAPP_DIRECTORY / "static"


events_blueprint = Blueprint('events_blueprint', __name__, template_folder=HTML_DIRECTORY, static_folder=STATIC_DIRECTORY)


@events_blueprint.get("/events")
@events_blueprint.get("/events/")
# @authorize
def GET_events():
	events = database.event.select_events()
	return render_template("events/index.j2", events=events)


@events_blueprint.get("/events/new")
# @authorize
def GET_events_new():
	return render_template("events/new.j2")


@events_blueprint.post("/events/new")
# @authorize
def POST_events_new():
	name = request.form.get("event_name-input")
	date = request.form.get("event_date-input")
	print(date)
	date = date_type.fromisoformat(date)
	event = Event(
		id=0,
		name=name,
		date=date,
		start=None,
		ended=None,
		rounds=None,
	)

	database.event.insert_event(event)

	return redirect(f"/events/{event.id}")


@events_blueprint.get("/events/<int:id>")
# @authorize
def GET_events_event(id: int):
	event: Event = database.event.select_event(id)

	return render_template("events/event/index.j2", event=event)


@events_blueprint.get("/events/<int:id>/rounds")
# @authorize
def GET_events_event_rounds(id: int):
	event: Event = database.event.select_event(id)

	return render_template("events/event/rounds/index.j2", event=event)


@events_blueprint.get("/events/<int:id>/rounds/new")
# @authorize
def GET_events_event_rounds_new(id: int):
	event: Event = database.event.select_event(id)
	playlist_sets: list[PlaylistSet] = database.playlist_set.select_playlist_sets()
	return render_template("events/event/rounds/new.j2", event=event, playlist_sets=playlist_sets)


@events_blueprint.post("/events/<int:id>/rounds/new")
# @authorize
def POST_events_event_rounds_new(id: int):
	playlist_set_id = int(request.form.get("playlist_set-select"))
	size_rows = int(request.form.get("round_size_rows-input"))
	size_columns = int(request.form.get("round_size_columns-input"))

	name = request.form.get("round_name-input")
	size = [size_rows, size_columns]

	round = Round(
		id=0,
		name=name,
		size=size,
		start=None,
		event=Event(id=id,name=None,date=None,start=None,ended=None,rounds=None),
		playlist_set=PlaylistSet(id=playlist_set_id, name=None, playlist=None, songs=None),
		cards=None,
	)

	database.round.insert_round(round)

	return redirect(f"/events/{id}/rounds/{round.id}")


@events_blueprint.get("/events/<int:event_id>/rounds/<int:round_id>")
# @authorize
def GET_events_event_rounds_round(event_id: int, round_id: int):
	round: Round = database.round.select_round(round_id)

	return render_template("events/event/rounds/round/index.j2", round=round)
