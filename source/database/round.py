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

#!/opt/homebrew/bin/python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2025.09.21                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


import psycopg2.extras


from database.connect import connect
from trinkgo.classes import Round, Card


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

	query = """SELECT * FROM "Cards" WHERE "Rounds.id" = %s AND "is_deleted" = FALSE;"""
	cursor.execute(query, (id,))
	round_dict["cards"] = list(map(Card.from_dict, cursor))

	round: Round = Round.from_dict(round_dict)
	return round


@connect
def select_rounds(cursor: psycopg2.extras.RealDictCursor) -> list[Round]:
	query = """SELECT * FROM "Rounds" WHERE "is_deleted" = FALSE;"""
	cursor.execute(query)
	return [Round.from_dict(round_dict) for round_dict in cursor]
