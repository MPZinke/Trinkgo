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
from webapp.router.events.rounds import rounds_blueprint


WEBAPP_DIRECTORY = Path(__file__).parents[2]
HTML_DIRECTORY = WEBAPP_DIRECTORY / "html"
STATIC_DIRECTORY = WEBAPP_DIRECTORY / "static"


events_blueprint = Blueprint('events_blueprint', __name__, template_folder=HTML_DIRECTORY, static_folder=STATIC_DIRECTORY)
events_blueprint.register_blueprint(rounds_blueprint)


@events_blueprint.get("/events")
@events_blueprint.get("/events/")
def GET_events():
	events = database.events.select_events()
	database.rounds.select_rounds_for_events(events)
	return render_template("events/index.j2", events=events)


@events_blueprint.get("/events/new")
def GET_events_new():
	return render_template("events/new.j2", date=date_type.today().strftime("%Y-%m-%d"))


@events_blueprint.post("/events/new")
def POST_events_new():
	name = request.form.get("event_name-input")
	date = request.form.get("event_date-input")
	date = date_type.fromisoformat(date)
	event = Event(
		id=0,
		name=name,
		date=date,
		start=None,
		ended=None,
		rounds=None,
	)

	database.events.insert_event(event)

	return redirect(f"/events/{event.id}")


@events_blueprint.get("/events/<int:id>")
def GET_events_event(id: int):
	event: Event = database.events.select_event(id)
	database.rounds.select_rounds_for_event(event)
	database.playlist_sets.select_playlist_sets_for_rounds(event.rounds)

	return render_template("events/event/index.j2", event=event)
