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
from trinkgo.classes import Event, Round


@connect
def insert_event(cursor: psycopg2.extras.RealDictCursor, event: Event):
	query = """INSERT INTO "Events" ("name", "date") VALUES (%s, %s) RETURNING "id";"""
	cursor.execute(query, (event.name, event.date))
	event.id = cursor.fetchone()["id"]


@connect
def select_event(cursor: psycopg2.extras.RealDictCursor, id: str) -> Event:
	query = """SELECT * FROM "Events" WHERE "id" = %s AND "is_deleted" = FALSE;"""
	cursor.execute(query, (id,))
	event_dict: dict = cursor.fetchone()

	event: Event = Event.from_dict(event_dict)
	return event


@connect
def select_event_and_rounds(cursor: psycopg2.extras.RealDictCursor, id: str) -> Event:
	query = """SELECT * FROM "Events" WHERE "id" = %s AND "is_deleted" = FALSE;"""
	cursor.execute(query, (id,))

	event: Event = Event.from_dict(cursor.fetchone())
	database.round.select_rounds_for_event(event)

	return event


@connect
def select_event_for_round(cursor: psycopg2.extras.RealDictCursor, round: Round) -> None:
	query = """
		SELECT *
		FROM "Events"
		WHERE "id" = (SELECT "Events.id" FROM "Rounds" WHERE "id" = %s);"""
	cursor.execute(query, (round.id,))

	round.event = Event.from_dict({"round": round, **cursor.fetchone()})


@connect
def select_events(cursor: psycopg2.extras.RealDictCursor) -> list[Event]:
	query = """SELECT * FROM "Events" WHERE "is_deleted" = FALSE;"""
	cursor.execute(query)
	return [Event.from_dict(event_dict) for event_dict in cursor]
