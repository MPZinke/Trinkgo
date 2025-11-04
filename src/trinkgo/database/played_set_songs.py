#!/opt/homebrew/bin/python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2025.10.28                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


import psycopg2.extras


from trinkgo.database.connect import connect
from trinkgo.spotify.classes import Playlist, Song
from trinkgo.game.classes import PlaylistSet, Round, SetSong


@connect
def insert_played_set_song(cursor: psycopg2.extras.RealDictCursor, set_song: SetSong, round: Round):
	query = """INSERT INTO "PlayedSongsSets" ("SongsSets.id", "Rounds.id") VALUES (%s, %s) RETURNING "id";"""
	cursor.execute(query, (set_song.id, round.id))
	if(round.played_set_songs is None):
		round.played_set_songs = []

	round.played_set_songs.insert(0, set_song)


@connect
def select_played_set_songs_for_round(cursor: psycopg2.extras.RealDictCursor, round: Round) -> None:
	query = """SELECT * FROM "PlayedSongsSets" WHERE "Rounds.id" = %s ORDER BY "id" DESC;"""
	cursor.execute(query, (round.id,))

	round.played_set_songs = []
	for card_song_dict in cursor:
		card_song_matches = lambda set_song: set_song.id == card_song_dict["SongsSets.id"]
		set_song = next(filter(card_song_matches, round.playlist_set.set_songs))
		round.played_set_songs.append(set_song)
