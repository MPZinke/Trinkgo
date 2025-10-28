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
import requests


import database
import spotify
from trinkgo.classes import Card, Event, PlaylistSet, Round
from webapp.router import app
from webapp.router.auth import authorize


WEBAPP_DIRECTORY = Path(__file__).parents[3]
HTML_DIRECTORY = WEBAPP_DIRECTORY / "html"
STATIC_DIRECTORY = WEBAPP_DIRECTORY / "static"


play_blueprint = Blueprint('play_blueprint', __name__, template_folder=HTML_DIRECTORY, static_folder=STATIC_DIRECTORY)


@play_blueprint.get("/events/<int:event_id>/rounds/<int:round_id>/play")
@authorize
def GET_events_event_rounds_round_play(event_id: int, round_id: int):
	round: Round = database.round.select_round(round_id)
	database.event.select_event_for_round(round)
	database.playlist_set.select_playlist_set_for_round(round)
	database.set_song.select_set_songs_for_playlist_set(round.playlist_set)
	database.card.select_cards_for_round(round)
	database.played_set_song.select_played_set_songs_for_round(round)

	return render_template("events/event/rounds/round/play/index.j2", round=round)
