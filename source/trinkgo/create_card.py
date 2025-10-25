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
from typing import Tuple


from spotify.classes import Song
from trinkgo.classes import Card, Round, SetSong


def random_songs(songs: list[Song], length: int, repeat: bool=False) -> list[SetSong]:
	card_songs = []
	while(len(card_songs) < 25):
		random_index = randint(0, len(songs)-1)
		song = songs[random_index]
		if(repeat or song not in card_songs):
			card_songs.append(song)

	return card_songs


def create_card(round: Round, size: Tuple[int, int], freespot: bool=True, repeat: bool=False):
	songs: list[SetSong] = random_songs(round.playlist_set.set_songs, size[0]*size[1] - int(freespot))

	card_songs = [[None for _ in size[1]] for _ in size[0]]
	for row in range(size[0]):
		for column in range(size[1]):
			if(freespot and row == size[0] // 2 and column == size[1]):
				continue

			card_songs[row][column] = songs.pop(0)

	card = Card(
		id=0,
		identifier=0,
		size=size,
		songs=card_songs,
		round=round,
	)
	# card = Card(playlist.title, random_songs(playlist.songs))
	# card.save()
