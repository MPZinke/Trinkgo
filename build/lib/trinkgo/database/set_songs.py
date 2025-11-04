#!/opt/homebrew/bin/python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2025.10.24                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


import psycopg2.extras


from trinkgo.database.connect import connect
from trinkgo.spotify.classes import Playlist, Song
from trinkgo.game.classes import PlaylistSet, SetSong


@connect
def select_set_song(cursor: psycopg2.extras.RealDictCursor, id: int):
	query = """
		SELECT
			"SongsSets".*,
			"Songs"."uri" AS "Songs.uri",
			"Songs"."title" AS "Songs.title",
			"Songs"."album" AS "Songs.album",
			"Songs"."artists" AS "Songs.artists",
			"Songs"."artwork" AS "Songs.artwork",
			"Songs"."length" AS "Songs.length",
			"Songs"."released" AS "Songs.released"
		FROM "SongsSets"
		JOIN "Songs" ON "SongsSets"."Songs.id" = "Songs"."id"
		WHERE "SongsSets"."id" = %s
		ORDER BY "id" ASC;
	"""
	cursor.execute(query, (id,))
	set_song_dict = cursor.fetchone()

	song = Song(
		id=set_song_dict["Songs.id"],
		uri=set_song_dict["Songs.uri"],
		title=set_song_dict["Songs.title"],
		album=set_song_dict["Songs.album"],
		artists=set_song_dict["Songs.artists"],
		artwork=set_song_dict["Songs.artwork"],
		length=set_song_dict["Songs.length"],
		released=set_song_dict["Songs.released"],
		playlist=None,
	)
	return SetSong.from_dict(song=song, **set_song_dict)


@connect
def select_set_songs_for_playlist_set(cursor: psycopg2.extras.RealDictCursor, playlist_set: PlaylistSet):
	query = """
		SELECT
			"SongsSets".*,
			"Songs"."uri" AS "Songs.uri",
			"Songs"."title" AS "Songs.title",
			"Songs"."album" AS "Songs.album",
			"Songs"."artists" AS "Songs.artists",
			"Songs"."artwork" AS "Songs.artwork",
			"Songs"."length" AS "Songs.length",
			"Songs"."released" AS "Songs.released"
		FROM "SongsSets"
		JOIN "Songs" ON "SongsSets"."Songs.id" = "Songs"."id"
		WHERE "SongsSets"."PlaylistsSets.id" = %s
		  AND "SongsSets"."is_deleted" = FALSE
		ORDER BY "id" ASC;
	"""
	cursor.execute(query, (playlist_set.id,))

	playlist_set.playlist.songs = []
	playlist_set.set_songs = []
	for set_song_dict in cursor:
		song = Song(
			id=set_song_dict["Songs.id"],
			uri=set_song_dict["Songs.uri"],
			title=set_song_dict["Songs.title"],
			album=set_song_dict["Songs.album"],
			artists=set_song_dict["Songs.artists"],
			artwork=set_song_dict["Songs.artwork"],
			length=set_song_dict["Songs.length"],
			released=set_song_dict["Songs.released"],
			playlist=playlist_set.playlist,
		)
		set_song = SetSong.from_dict(song=song, playlist_set=playlist_set, **set_song_dict)
		playlist_set.set_songs.append(set_song)
		playlist_set.playlist.songs.append(song)


@connect
def update_set_song(cursor: psycopg2.extras.RealDictCursor, set_song: SetSong) -> None:
	query = """
		UPDATE "SongsSets"
		SET "label" = %s, "start" = %s, "duration" = %s
		WHERE "id" = %s;
	"""
	cursor.execute(query, (set_song.label, set_song.start, set_song.duration, set_song.id))
