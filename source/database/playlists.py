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
from spotify.classes import Playlist, Song


@connect
def insert_playlist(cursor: psycopg2.extras.RealDictCursor, playlist: Playlist):
	query = """INSERT INTO "Playlists" ("uri", "title") VALUES (%s, %s) RETURNING "id";"""
	cursor.execute(query, (playlist.uri, playlist.title))
	playlist.id = cursor.fetchone()["id"]

	query = """
		INSERT INTO "Songs" ("uri", "title", "album", "artists", "artwork", "length", "released", "Playlists.id")
		SELECT
			"Temp"."uri",
			"Temp"."title",
			"Temp"."album",
			"Temp"."artists",
			"Temp"."artwork",
			"Temp"."length",
			"Temp"."released",
			%s
		FROM UNNEST(%s, %s, %s, %s, %s, %s, %s)
		  AS "Temp" ("uri", "title", "album", "artists", "artwork", "length", "released")
		RETURNING "id";
	"""

	unnest_values = {"uri": [], "title": [], "album": [], "artists": [], "artwork": [], "length": [], "released": []}
	for song in playlist.songs:
		for key, value in unnest_values.items():
			value.append(getattr(song, key))

	cursor.execute(query, (playlist.id, *unnest_values.values()))

	for playlist_song, song in zip(playlist.songs, cursor):
		playlist_song.id = song["id"]


@connect
def select_playlist(cursor: psycopg2.extras.RealDictCursor, id: str) -> Playlist:
	query = """SELECT * FROM "Playlists" WHERE "id" = %s AND "is_deleted" = FALSE;"""
	cursor.execute(query, (id,))
	playlist: Playlist = Playlist.from_dict(**cursor.fetchone())

	query = """SELECT * FROM "Songs" WHERE "Playlists.id" = %s AND "is_deleted" = FALSE;"""
	cursor.execute(query, (id,))
	playlist.songs = [Song.from_dict(playlist=playlist, **song_dict) for song_dict in cursor]

	return playlist


@connect
def select_playlists(cursor: psycopg2.extras.RealDictCursor) -> list[Playlist]:
	query = """SELECT * FROM "Playlists" WHERE "is_deleted" = FALSE;"""
	cursor.execute(query)
	return [Playlist.from_dict(**playlist_dict) for playlist_dict in cursor]
