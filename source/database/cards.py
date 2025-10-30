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
from trinkgo.classes import Card, CardSetSongs, Event, PlaylistSet, Round


@connect
def insert_card(cursor: psycopg2.extras.RealDictCursor, card: Card):
	query = """
		INSERT INTO "Cards" ("identifier", "size", "Rounds.id")
		VALUES (%s, %s, %s) RETURNING "id";
	"""
	cursor.execute(query, (card.identifier, card.size, card.round.id))
	card.id = cursor.fetchone()["id"]

	query = """
		INSERT INTO "CardsSongsSets" ("position", "SongsSets.id", "Cards.id")
		SELECT ARRAY["Temp"."position_x", "Temp"."position_y"]::INTEGER[2], "Temp"."SongsSets.id", "Temp"."Cards.id"
		FROM UNNEST(%s, %s, %s, %s)
		  AS "Temp" ("position_x", "position_y", "SongsSets.id", "Cards.id")
		RETURNING "id";
	"""

	unnest_values = {"position_x": [], "position_y": [], "SongsSets.id": [], "Cards.id": []}
	for row_index, row in enumerate(card.set_songs):
		for column_index, set_song in enumerate(row):
			if(set_song is not None):
				unnest_values["position_x"].append(row_index)
				unnest_values["position_y"].append(column_index)
				unnest_values["SongsSets.id"].append(set_song.id)
				unnest_values["Cards.id"].append(card.id)

	cursor.execute(query, tuple(unnest_values.values()))


@connect
def insert_cards(cursor: psycopg2.extras.RealDictCursor, cards: list[Card]):
	if(len(cards) == 0):
		return

	query = """
		INSERT INTO "Cards" ("identifier", "size", "Rounds.id")
		SELECT
			(
				SELECT TO_HEX(COUNT(id)+"increment") FROM "Cards" WHERE "Rounds.id" = %(round_id)s
			),
			%(size)s,
			%(round_id)s
		FROM GENERATE_SERIES(1, %(length)s) AS "increment"  -- FROM: https://stackoverflow.com/a/48176915
		RETURNING "id";
	"""
	cursor.execute(query, {"round_id": cards[0].round.id, "size": cards[0].size, "length": len(cards)})

	for card, card_dict in zip(cards, cursor):
		card.id = card_dict["id"]

	query = """
		INSERT INTO "CardsSongsSets" ("position", "SongsSets.id", "Cards.id")
		SELECT ARRAY["Temp"."position_x", "Temp"."position_y"]::INTEGER[2], "Temp"."SongsSets.id", "Temp"."Cards.id"
		FROM UNNEST(%s, %s, %s, %s)
		  AS "Temp" ("position_x", "position_y", "SongsSets.id", "Cards.id")
		RETURNING "id";
	"""

	unnest_values = {"position_x": [], "position_y": [], "SongsSets.id": [], "Cards.id": []}
	for card in cards:
		for row_index, row in enumerate(card.set_songs):
			for column_index, set_song in enumerate(row):
				if(set_song is not None):
					unnest_values["position_x"].append(row_index)
					unnest_values["position_y"].append(column_index)
					unnest_values["SongsSets.id"].append(set_song.id)
					unnest_values["Cards.id"].append(card.id)

	cursor.execute(query, tuple(unnest_values.values()))


@connect
def select_card(cursor: psycopg2.extras.RealDictCursor, id: str) -> Card:
	query = """
		SELECT *
		FROM "Cards"
		WHERE "id" = %s;
	"""
	cursor.execute(query, (id,))
	card_dict: dict = cursor.fetchone()

	return Card.from_dict(set_songs=CardSetSongs(card_dict["size"]), **card_dict)


@connect
def select_cards_for_round(cursor: psycopg2.extras.RealDictCursor, round: Round) -> None:
	query = """SELECT * FROM "Cards" WHERE "Rounds.id" = %s AND "is_deleted" = FALSE;"""
	cursor.execute(query, (round.id,))

	round.cards = [Card.from_dict(set_songs=CardSetSongs(round.size), round=round, **card_dict) for card_dict in cursor]


@connect
def select_card_songs(cursor: psycopg2.extras.RealDictCursor, card: Card, playlist_set: PlaylistSet) -> None:
	query = """SELECT * FROM "CardsSongsSets" WHERE "Cards.id" = %s;"""
	cursor.execute(query, (card.id,))

	for card_song_dict in cursor:
		set_song = next(set_song for set_song in playlist_set.set_songs if(set_song.id == card_song_dict["SongsSets.id"]))
		position = card_song_dict["position"]
		card.set_songs[position] = set_song


@connect
def select_cards_songs(
	cursor: psycopg2.extras.RealDictCursor,
	cards: list[Card],
	playlist_set: PlaylistSet
) -> None:
	query = """
		SELECT *
		FROM "CardsSongsSets"
		WHERE "Cards.id" IN %s;
	"""
	cards_ids = (0, *[card.id for card in cards])  # Mitigate empty cards SQL syntax issue
	cursor.execute(query, (cards_ids,))
	card_song_dicts = list(map(dict, cursor))

	for card in cards:
		for card_song_dict in card_song_dicts:
			if card_song_dict["Cards.id"] != card.id:
				continue

			set_song = next(set_song for set_song in playlist_set.set_songs if(set_song.id == card_song_dict["SongsSets.id"]))
			position = card_song_dict["position"]
			card.set_songs[position] = set_song
