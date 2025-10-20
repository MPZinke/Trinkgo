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


import psycopg2.extras


from database.connect import connect
import database
from trinkgo.classes import Card, Event, PlaylistSet, Round


@connect
def insert_card(cursor: psycopg2.extras.RealDictCursor, card: Card):
	query = """
		INSERT INTO "Cards" ("name", "size", "Events.id", "PlaylistsSets.id")
		VALUES (%s, %s, %s, %s) RETURNING "id";
	"""
	cursor.execute(query, (card.name, card.size, card.event.id, card.playlist_set.id))
	card.id = cursor.fetchone()["id"]


@connect
def select_card(cursor: psycopg2.extras.RealDictCursor, id: str) -> Card:
	query = """SELECT * FROM "Cards" WHERE "id" = %s AND "is_deleted" = FALSE;"""
	cursor.execute(query, (id,))
	card_dict: dict = cursor.fetchone()

	card: Card = Card.from_dict(card_dict)
	return card


@connect
def select_cards(cursor: psycopg2.extras.RealDictCursor) -> list[Card]:
	query = """SELECT * FROM "Cards" WHERE "is_deleted" = FALSE;"""
	cursor.execute(query)
	return [Card.from_dict(card_dict) for card_dict in cursor]


@connect
def select_cards_for_round(cursor: psycopg2.extras.RealDictCursor, round: Round) -> None:
	query = """SELECT * FROM "Cards" WHERE "Rounds.id" = %s AND "is_deleted" = FALSE;"""
	cursor.execute(query, (round.id,))

	round.cards = [Card.from_dict({**card_dict, "round": round}) for card_dict in cursor]
