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


from flask import redirect, render_template, request, Blueprint
from flask_login import login_required
import requests


from trinkgo import database
from trinkgo import spotify
from trinkgo.game.classes import Event, PlaylistSet, Round
from trinkgo.webapp.router.events.rounds import rounds_blueprint


events_blueprint = Blueprint('events_blueprint', __name__)
events_blueprint.register_blueprint(rounds_blueprint)


@events_blueprint.get("/events")
@events_blueprint.get("/events/")
@login_required
def GET_events():
	events = database.events.select_events()
	database.rounds.select_rounds_for_events(events)
	return render_template("events/index.j2", events=events)


@events_blueprint.get("/events/new")
@login_required
def GET_events_new():
	return render_template("events/new.j2", date=date_type.today().strftime("%Y-%m-%d"))


@events_blueprint.post("/events/new")
@login_required
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
@login_required
def GET_events_event(id: int):
	event: Event = database.events.select_event(id)
	database.rounds.select_rounds_for_event(event)
	database.playlist_sets.select_playlist_sets_for_rounds(event.rounds)

	return render_template("events/event/index.j2", event=event)
