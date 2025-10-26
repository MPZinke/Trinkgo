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
from io import BytesIO
from pathlib import Path


from flask import redirect, render_template, request, send_file, Blueprint
import requests


import database
import spotify
from trinkgo.create_card import create_card
from trinkgo.classes import Card, Event, PlaylistSet, Round
from webapp.router import app
from webapp.router.auth import authorize


WEBAPP_DIRECTORY = Path(__file__).parents[3]
HTML_DIRECTORY = WEBAPP_DIRECTORY / "html"
STATIC_DIRECTORY = WEBAPP_DIRECTORY / "static"


cards_blueprint = Blueprint('cards_blueprint', __name__, template_folder=HTML_DIRECTORY, static_folder=STATIC_DIRECTORY)


@cards_blueprint.get("/events/<int:event_id>/rounds/<int:round_id>/cards")
def GET_events_event_rounds_round_cards(event_id: int, round_id: int):
	round: Round = database.round.select_round(round_id)
	database.event.select_event_for_round(round)
	database.playlist_set.select_playlist_set_for_round(round)
	database.card.select_cards_for_round(round)

	return render_template("events/event/rounds/round/cards.j2", round=round)


@cards_blueprint.post("/events/<int:event_id>/rounds/<int:round_id>/cards/new")
def POST_events_event_rounds_round_cards_new(event_id: int, round_id: int):
	number_of_cards: int = int(request.form.get("number_of_cards-input"))

	round: Round = database.round.select_round(round_id)
	database.event.select_event_for_round(round)
	database.playlist_set.select_playlist_set_for_round(round)
	database.set_song.select_set_songs_for_playlist_set(round.playlist_set)
	database.card.select_cards_for_round(round)
	database.card.select_cards_songs(round.cards, round.playlist_set)

	card = create_card(round)

	return redirect(f"/events/{event_id}/rounds/{round_id}/cards/{card.id}")


@cards_blueprint.get("/events/<int:event_id>/rounds/<int:round_id>/cards/all")
def GET_events_event_rounds_round_cards_all(event_id: int, round_id: int):
	round: Round = database.round.select_round(round_id)
	database.event.select_event_for_round(round)
	database.playlist_set.select_playlist_set_for_round(round)
	database.set_song.select_set_songs_for_playlist_set(round.playlist_set)
	database.card.select_cards_for_round(round)
	database.card.select_cards_songs(round.cards, round.playlist_set)

	card_images = [card.image() for card in round.cards]
	pdf = Card.pdf(card_images)
	return send_file(pdf, download_name=f"{round.name}.pdf", mimetype="application/pdf")


@cards_blueprint.get("/events/<int:event_id>/rounds/<int:round_id>/cards/<int:card_id>")
def GET_events_event_rounds_round_cards_card(event_id: int, round_id: int, card_id: int):
	card: Card = database.card.select_card(card_id)
	database.round.select_round_for_card(card)
	database.event.select_event_for_round(card.round)
	database.playlist_set.select_playlist_set_for_round(card.round)
	database.set_song.select_set_songs_for_playlist_set(card.round.playlist_set)
	database.card.select_card_songs(card, card.round.playlist_set)

	pdf: BytesIO = Card.pdf(card.image())
	return send_file(pdf, download_name=f"{card.identifier}.pdf", mimetype="application/pdf")
