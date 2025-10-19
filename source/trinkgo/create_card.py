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


from random import randint


from spotify.classes import Song


def random_songs(length: int, songs: list[Song], repeat: bool=False) -> list[Song]:
	card_songs = []
	while(len(card_songs) < 25):
		random_index = randint(0, len(songs)-1)
		song = songs[random_index]
		if(repeat or song not in card_songs):
			card_songs.append(song)

	return card_songs


def create_card(playlist_id: str):
	pass
	# card = Card(playlist.name, random_songs(playlist.songs))
	# card.save()
