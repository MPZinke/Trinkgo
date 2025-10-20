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


import database
from database.connect import connect
from spotify.classes import Playlist, Song


@connect
def insert_playlist(cursor: psycopg2.extras.RealDictCursor, playlist: Playlist):
	query = """INSERT INTO "Playlists" ("uri", "name") VALUES (%s, %s) RETURNING "id";"""
	cursor.execute(query, (playlist.uri, playlist.name))
	playlist.id = cursor.fetchone()["id"]

	query = """
		INSERT INTO "Songs" ("uri", "name", "album", "artists", "artwork", "length", "Playlists.id")
		SELECT "Temp"."uri", "Temp"."name", "Temp"."album", "Temp"."artists", "Temp"."artwork", "Temp"."length", %s
		FROM UNNEST(%s, %s, %s, %s, %s, %s) 
		  AS "Temp" ("uri", "name", "album", "artists", "artwork", "length")
		RETURNING "id";
	"""

	uris: list[str] = [song.uri for song in playlist.songs]
	names: list[str] = [song.name for song in playlist.songs]
	albums: list[str] = [song.album for song in playlist.songs]
	artists: list[str] = [song.artists for song in playlist.songs]
	artworks: list[str] = [song.artwork for song in playlist.songs]
	lengths: list[str] = [song.length for song in playlist.songs]

	cursor.execute(query, (playlist.id, uris, names, albums, artists, artworks, lengths))

	for playlist_song, song in zip(playlist.songs, cursor):
		playlist_song.id = song["id"]


@connect
def select_playlist(cursor: psycopg2.extras.RealDictCursor, id: str) -> Playlist:
	query = """SELECT * FROM "Playlists" WHERE "id" = %s AND "is_deleted" = FALSE;"""
	cursor.execute(query, (id,))
	playlist: Playlist = Playlist.from_dict(cursor.fetchone())

	query = """SELECT * FROM "Songs" WHERE "Playlists.id" = %s AND "is_deleted" = FALSE;"""
	cursor.execute(query, (id,))
	playlist.songs = [Song.from_dict({**song_dict, "playlist": playlist}) for song_dict in cursor]

	return playlist


@connect
def select_playlist_and_songs(cursor: psycopg2.extras.RealDictCursor, id: str) -> Playlist:
	query = """SELECT * FROM "Playlists" WHERE "id" = %s AND "is_deleted" = FALSE;"""
	cursor.execute(query, (id,))

	playlist: Playlist = Playlist.from_dict(cursor.fetchone())
	database.song.select_songs_for_playlist(playlist)

	return playlist


@connect
def select_playlists(cursor: psycopg2.extras.RealDictCursor) -> list[Playlist]:
	query = """SELECT * FROM "Playlists" WHERE "is_deleted" = FALSE;"""
	cursor.execute(query)
	return [Playlist.from_dict(playlist_dict) for playlist_dict in cursor]
