#!/opt/homebrew/bin/python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2025.10.19                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


import psycopg2.extras


from database.connect import connect
from trinkgo.classes import Card, Event, PlaylistSet, Round


@connect
def insert_round(cursor: psycopg2.extras.RealDictCursor, round: Round):
	query = """
		INSERT INTO "Rounds" ("name", "size", "Events.id", "PlaylistsSets.id")
		VALUES (%s, %s, %s, %s) RETURNING "id";
	"""
	cursor.execute(query, (round.name, round.size, round.event.id, round.playlist_set.id))
	round.id = cursor.fetchone()["id"]


@connect
def select_round(cursor: psycopg2.extras.RealDictCursor, id: str) -> Round:
	query = """SELECT * FROM "Rounds" WHERE "id" = %s AND "is_deleted" = FALSE;"""
	cursor.execute(query, (id,))
	round_dict: dict = cursor.fetchone()

	round: Round = Round.from_dict(round_dict)
	return round


@connect
def select_round_all(cursor: psycopg2.extras.RealDictCursor, id: str) -> Round:
	query = """SELECT * FROM "Rounds" WHERE "id" = %s AND "is_deleted" = FALSE;"""
	cursor.execute(query, (id,))
	round_dict: dict = cursor.fetchone()
	round: Round = Round.from_dict(round_dict)

	round.event = database.event.select_event(round_dict["Events.id"])
	round.playlist_set = database.playlist_set.select_playlist_set(round_dict["PlaylistsSets.id"])
	database.cards.select_cards_for_round(round)

	return round


@connect
def select_rounds(cursor: psycopg2.extras.RealDictCursor) -> list[Round]:
	query = """SELECT * FROM "Rounds" WHERE "is_deleted" = FALSE;"""
	cursor.execute(query)
	return [Round.from_dict(round_dict) for round_dict in cursor]


@connect
def select_rounds_for_event(cursor: psycopg2.extras.RealDictCursor, event: Event) -> None:
	query = """SELECT * FROM "Rounds" WHERE "Events.id" = %s AND "is_deleted" = FALSE;"""
	cursor.execute(query, (event.id,))
	event.rounds = [Round.from_dict({**round_dict, "event": event}) for round_dict in cursor]
