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


from database.connect import connect
from spotify.classes import Playlist, Song
from trinkgo.classes import PlaylistSet, SetSong


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
		set_song = SetSong.from_dict({**set_song_dict, "song": song, "playlist_set": playlist_set})
		playlist_set.set_songs.append(set_song)
		playlist_set.playlist.songs.append(song)
