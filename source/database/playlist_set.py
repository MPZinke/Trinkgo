#!/opt/homebrew/bin/python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2025.10.05                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


import psycopg2.extras


from database.connect import connect
from spotify.classes import Playlist, Song
from trinkgo.classes import PlaylistSet, Round, SetSong


@connect
def insert_set(cursor: psycopg2.extras.RealDictCursor, playlist_set: PlaylistSet):
	query = """INSERT INTO "PlaylistsSets" ("name", "Playlists.id") VALUES (%s, %s) RETURNING "id";"""
	cursor.execute(query, (playlist_set.name, playlist_set.playlist.id))
	playlist_set.id = cursor.fetchone()["id"]

	query = """
		INSERT INTO "SongsSets" ("start", "duration", "label", "Songs.id", "PlaylistsSets.id")
		SELECT 0, "Songs"."length", '', "Songs".id, %s
		FROM "Songs"
		WHERE "Playlists.id" = %s
		  AND "is_deleted" = FALSE
		RETURNING "id";
	"""

	cursor.execute(query, (playlist_set.id, playlist_set.playlist.id))


@connect
def select_playlist_set(cursor: psycopg2.extras.RealDictCursor, id: str) -> Playlist:
	query = """
		SELECT
			"PlaylistsSets".*,
			"Playlists"."title" AS "Playlists.title",
			"Playlists"."uri" AS "Playlists.uri"
		FROM "PlaylistsSets" 
		JOIN "Playlists" ON "PlaylistsSets"."Playlists.id" = "Playlists"."id"
		WHERE "PlaylistsSets"."id" = %s;
	"""
	cursor.execute(query, (id,))
	playlist_set_dict = cursor.fetchone()

	playlist = Playlist(
		id=playlist_set_dict["Playlists.id"],
		title=playlist_set_dict["Playlists.title"],
		uri=playlist_set_dict["Playlists.uri"],
		songs=None,
	)
	return PlaylistSet.from_dict({**playlist_set_dict, "playlist": playlist})


@connect
def select_playlist_set_for_round(cursor: psycopg2.extras.RealDictCursor, round: Round) -> Playlist:
	query = """
		SELECT
			"PlaylistsSets".*,
			"Playlists"."title" AS "Playlists.title",
			"Playlists"."uri" AS "Playlists.uri"
		FROM "Rounds"
		JOIN "PlaylistsSets" ON "Rounds"."PlaylistsSets.id" = "PlaylistsSets"."id"
		JOIN "Playlists" ON "PlaylistsSets"."Playlists.id" = "Playlists"."id"
		WHERE "Rounds"."id" = %s;
	"""
	cursor.execute(query, (round.id,))
	playlist_set_dict = cursor.fetchone()

	playlist = Playlist(
		id=playlist_set_dict["Playlists.id"],
		title=playlist_set_dict["Playlists.title"],
		uri=playlist_set_dict["Playlists.uri"],
		songs=None,
	)
	round.playlist_set = PlaylistSet.from_dict({**playlist_set_dict, "playlist": playlist})


@connect
def select_playlist_sets(cursor: psycopg2.extras.RealDictCursor) -> list[Playlist]:
	query = """SELECT * FROM "PlaylistsSets" WHERE "is_deleted" = FALSE;"""
	cursor.execute(query)
	return [PlaylistSet(id=playlist_dict["id"], name=playlist_dict["name"], playlist=None, set_songs=[]) for playlist_dict in cursor]
