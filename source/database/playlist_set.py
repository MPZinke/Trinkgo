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
from trinkgo.classes import PlaylistSet, SetSong


@connect
def insert_set(cursor: psycopg2.extras.RealDictCursor, playlist_set: PlaylistSet):
	query = """INSERT INTO "PlaylistsSets" ("name", "Playlists.id") VALUES (%s, %s) RETURNING "id";"""
	cursor.execute(query, (playlist_set.name, playlist_set.playlist.id))
	playlist_set.id = cursor.fetchone()["id"]

	query = """
		INSERT INTO "SongsSets" ("start", "duration", "Songs.id", "PlaylistsSets.id")
		SELECT 0, "Songs"."length", "Songs".id, %s
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
			"Playlists"."name" AS "Playlists.name",
			"Playlists"."uri" AS "Playlists.uri"
		FROM "PlaylistsSets" 
		JOIN "Playlists" ON "PlaylistsSets"."Playlists.id" = "Playlists"."id"
		WHERE "PlaylistsSets"."id" = %s
		  AND "PlaylistsSets"."is_deleted" = FALSE;
	"""
	cursor.execute(query, (id,))
	playlist_set: PlaylistSet = PlaylistSet.from_dict(cursor.fetchone())

	query = """
		SELECT
			"SongsSets".*,
			"Songs"."uri" AS "Songs.uri",
			"Songs"."name" AS "Songs.name",
			"Songs"."album" AS "Songs.album",
			"Songs"."artists" AS "Songs.artists",
			"Songs"."artwork" AS "Songs.artwork",
			"Songs"."length" AS "Songs.length"
		FROM "SongsSets" 
		JOIN "Songs" ON "SongsSets"."Songs.id" = "Songs"."id"
		WHERE "SongsSets"."PlaylistsSets.id" = %s
		  AND "SongsSets"."is_deleted" = FALSE;
	"""

	cursor.execute(query, (id,))
	for set_song_dict in cursor:
		playlist_set.songs.append(
			SetSong.from_dict(
				{**set_song_dict, "Songs.playlist": playlist_set.playlist, "playlist_set": playlist_set}
			)
		)

	return playlist_set


@connect
def select_playlist_sets(cursor: psycopg2.extras.RealDictCursor) -> list[Playlist]:
	query = """SELECT * FROM "PlaylistsSets" WHERE "is_deleted" = FALSE;"""
	cursor.execute(query)
	return [PlaylistSet(id=playlist_dict["id"], name=playlist_dict["name"], playlist=None, songs=[]) for playlist_dict in cursor]
