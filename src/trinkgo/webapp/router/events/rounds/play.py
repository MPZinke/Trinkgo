#!/opt/homebrew/bin/python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2025.10.26                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


from pathlib import Path


from flask import redirect, render_template, Blueprint
from flask_login import login_required
import requests


from trinkgo import database
from trinkgo.game.classes import Round


WEBAPP_DIRECTORY = Path(__file__).parents[3]
HTML_DIRECTORY = WEBAPP_DIRECTORY / "html"
STATIC_DIRECTORY = WEBAPP_DIRECTORY / "static"


play_blueprint = Blueprint('play_blueprint', __name__, template_folder=HTML_DIRECTORY, static_folder=STATIC_DIRECTORY)


@play_blueprint.get("/events/<int:event_id>/rounds/<int:round_id>/play")
@login_required
def GET_events_event_rounds_round_play(_event_id: int, round_id: int):
	round: Round = database.rounds.select_round(round_id)

	if(round.start is None):
		database.rounds.update_round_start(round)

	database.events.select_event_for_round(round)
	database.playlist_sets.select_playlist_set_for_round(round)
	database.set_songs.select_set_songs_for_playlist_set(round.playlist_set)
	database.cards.select_cards_for_round(round)
	database.played_set_songs.select_played_set_songs_for_round(round)

	return render_template("events/event/rounds/round/play/index.j2", round=round)


@play_blueprint.post("/events/<int:event_id>/rounds/<int:round_id>/end")
@login_required
def POST_events_event_rounds_round_end(event_id: int, round_id: int):
	database.rounds.update_round_ended(round_id)

	return redirect(f"/events/{event_id}/rounds/{round_id}")
