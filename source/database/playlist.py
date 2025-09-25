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
	query = """INSERT INTO "Playlists" ("id", "name") VALUES (%s, %s);"""
	cursor.execute(query, (playlist.id, playlist.name))

	query = """
		INSERT INTO "Songs" ("id", "name", "album", "artists", "artwork", "start", "duration", "Playlists.id")
		SELECT "Temp"."id", "Temp"."name", "Temp"."album", "Temp"."artists", "Temp"."artwork", "Temp"."start",
			"Temp"."duration", %s
		FROM UNNEST(%s, %s, %s, %s, %s, %s, %s) 
		  	AS "Temp" ("id", "name", "album", "artists", "artwork", "start", "duration");
	"""

	ids: list[str] = [song.id for song in playlist.songs]
	names: list[str] = [song.name for song in playlist.songs]
	albums: list[str] = [song.album for song in playlist.songs]
	artists: list[str] = [song.artists for song in playlist.songs]
	artworks: list[str] = [song.artwork for song in playlist.songs]
	starts: list[int] = [song.start for song in playlist.songs]
	durations: list[int] = [song.duration for song in playlist.songs]

	cursor.execute(query, (playlist.id, ids, names, albums, artists, artworks, starts, durations))


@connect
def select_playlist(cursor: psycopg2.extras.RealDictCursor, id: str) -> Playlist:
	query = """SELECT * FROM "Songs" WHERE "Playlists.id" = %s AND "is_deleted" = FALSE;"""
	cursor.execute(query, (id,))
	songs = [Song.from_dict(song_dict) for song_dict in cursor]

	query = """SELECT * FROM "Playlists" WHERE "id" = %s AND "is_deleted" = FALSE;"""
	cursor.execute(query, (id,))
	playlist_dict = cursor.fetchone()

	return Playlist(playlist_dict["id"], playlist_dict["name"], songs)


@connect
def select_playlists(cursor: psycopg2.extras.RealDictCursor) -> list[Playlist]:
	query = """SELECT * FROM "Playlists" WHERE "is_deleted" = FALSE;"""
	cursor.execute(query)
	return [Playlist.from_dict(playlist_dict) for playlist_dict in cursor]
