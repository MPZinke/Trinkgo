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


from datetime import date as date_type
from io import BytesIO
from pathlib import Path


from flask import redirect, render_template, request, send_file, Blueprint
from flask_login import current_user, login_required
import requests


from trinkgo import database
from trinkgo import spotify
from trinkgo.game.classes import Card, Event, PlaylistSet, Round


WEBAPP_DIRECTORY = Path(__file__).parents[3]
HTML_DIRECTORY = WEBAPP_DIRECTORY / "html"
STATIC_DIRECTORY = WEBAPP_DIRECTORY / "static"


play_blueprint = Blueprint('play_blueprint', __name__, template_folder=HTML_DIRECTORY, static_folder=STATIC_DIRECTORY)


@play_blueprint.get("/events/<int:event_id>/rounds/<int:round_id>/play")
@login_required
def GET_events_event_rounds_round_play(event_id: int, round_id: int):
	# TODO: Start round
	round: Round = database.rounds.select_round(round_id)
	database.events.select_event_for_round(round)
	database.playlist_sets.select_playlist_set_for_round(round)
	database.set_songs.select_set_songs_for_playlist_set(round.playlist_set)
	database.cards.select_cards_for_round(round)
	database.played_set_songs.select_played_set_songs_for_round(round)

	print(round.played_set_songs)

	return render_template("events/event/rounds/round/play/index.j2", round=round)
