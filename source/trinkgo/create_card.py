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


import database
from spotify.classes import Song
from trinkgo.classes import Card, CardSetSongs, Round, SetSong


def random_songs(songs: list[Song], length: int, repeat: bool=False) -> list[SetSong]:
	card_songs = []
	while(len(card_songs) < length):
		random_index = randint(0, len(songs)-1)
		song = songs[random_index]
		if(repeat or song not in card_songs):
			card_songs.append(song)

	return card_songs


def create_card(round: Round, freespot: bool=True, repeat: bool=False):
	songs: list[SetSong] = random_songs(round.playlist_set.set_songs, round.size[0]*round.size[1] - int(freespot))
	card_songs = CardSetSongs(round.size)
	for row in range(round.size[0]):
		for column in range(round.size[1]):
			if(freespot and row == round.size[0] // 2 and column == round.size[1] // 2):
				continue

			card_songs[row][column] = songs.pop(0)

	return Card(
		id=0,
		identifier=1,
		size=round.size,
		set_songs=card_songs,
		round=round,
	)


def create_cards(round: Round, number_of_cards: int, freespot: bool=True, repeat: bool=False) -> bool:
	cards: list[Card] = []

	for x in range(number_of_cards):
		while((card := create_card(round, freespot, repeat)) in cards or card in round.cards):
			...

		cards.append(card)

	database.card.insert_cards(cards)

	return cards
