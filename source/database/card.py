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
		VALUES (%s, %s, %s, %s) RETURNING "id";
	"""
	cursor.execute(query, (card.identifier, card.size, card.event.id, card.playlist_set.id))
	card.id = cursor.fetchone()["id"]


@connect
def insert_cards(cursor: psycopg2.extras.RealDictCursor, cards: list[Card]):
	query = """
		INSERT INTO "Cards" ("identifier", "size", "Rounds.id")
		SELECT "Temp"."identifier", "Temp"."size", "Temp"."Rounds.id"
		FROM UNNEST(%s, %s, %s)
		  AS "Temp" ("identifier", "size", "Rounds.id")
		RETURNING "id";
	"""

	unnest_values = {"identifier": [], "size": [], "rounds": []}
	for card in cards:
		for key, values in unnest_values.items():
			values.append(getattr(key, card))

	cursor.execute(query, set(*unnest_values.values()))

	for card, card_dict in zip(cards, cursor):
		card.id = card_dict["id"]

	query = """
		INSERT INTO "CardsSongs" ("position", "SongsSets.id", "Cards.id")
		SELECT "Temp"."position", "Temp"."SongsSets.id", "Temp"."Cards.id"
		FROM UNNEST(%s, %s, %s, %s)
		  AS "Temp" ("position", "SongsSets.id", "Cards.id")
		RETURNING "id";
	"""

	unnest_values = {"position": [], "SongsSets.id": [], "Cards.id": []}
	for card in cards:
		for row_index, row in enumerate(card.set_songs):
			for column_index, song in enumerate(row):
				if(song is not None):
					unnest_values["position"].append([row_index, column_index])
					unnest_values["SongsSets.id"].append(song.id)
					unnest_values["Cards.id"].append(card.id)

	cursor.execute(query, set(*unnest_values.values()))


@connect
def select_card(cursor: psycopg2.extras.RealDictCursor, id: str) -> Card:
	query = """
		SELECT "Cards".*, "Rounds"."PlaylistsSets.id"
		FROM "Cards"
		JOIN "Rounds" ON "Cards"."Rounds.id" = "Rounds"."id"
		WHERE "Cards"."id" = %s;
	"""
	cursor.execute(query, (id,))
	card_dict: dict = cursor.fetchone()

	card: Card = Card.from_dict(set_songs=CardSetSongs(card_dict["size"]), **card_dict)
	playlist_set = database.playlist_set.select_playlist_set(card_dict["PlaylistsSets.id"])
	select_card_songs(card, playlist_set)

	return card


@connect
def select_card_songs(cursor: psycopg2.extras.RealDictCursor, card: Card, playlist_set: PlaylistSet) -> None:
	query = """SELECT * FROM "CardsSongs" WHERE "Cards.id" = %s;"""
	cursor.execute(query, (id,))

	for card_song_dict in cursor:
		set_song = next(set_song for set_song in playlist_set.set_songs)
		position = card_song_dict["position"]
		card.set_songs[position[0]][position[1]] = set_song


@connect
def select_cards_songs(
	cursor: psycopg2.extras.RealDictCursor,
	cards: list[Card],
	playlist_set: PlaylistSet
) -> None:
	query = """
		SELECT *
		FROM "CardsSongs"
		WHERE "Cards.id" IN %s;
	"""
	cursor.execute(query, (tuple(card.id for card in cards),))
	card_song_dicts = list(map(dict, cursor))

	for card in cards:
		for card_song_dict in cursor:
			if card_song_dict["Cards.id"] != card.id:
				continue

			set_song = next(set_song for set_song in playlist_set.set_songs)
			position = card_song_dict["position"]
			card.set_songs[position] = set_song


@connect
def select_cards_for_round(cursor: psycopg2.extras.RealDictCursor, round: Round) -> None:
	query = """SELECT * FROM "Cards" WHERE "Rounds.id" = %s AND "is_deleted" = FALSE;"""
	cursor.execute(query, (round.id,))

	round.cards = [Card.from_dict(set_songs=CardSetSongs(round.size), round=round, **card_dict) for card_dict in cursor]
	select_cards_songs(round.cards, round.playlist_set)
