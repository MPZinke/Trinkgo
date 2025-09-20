#!/opt/homebrew/bin/python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2025.06.01                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


from random import randint


from webapp.router import app

from spotify import requests
from spotify.classes import Playlist, Song
from card import Card


def random_songs(songs: list[Song]) -> list[Song]:
	card_songs = []
	while(len(card_songs) < 25):
		random_index = randint(0, len(songs)-1)
		song = songs[random_index]
		if(song not in card_songs):
			card_songs.append(song)

	return card_songs


def main():
	app.run(host="0.0.0.0", port=8080, debug=True)

	# auth_token: str = requests.get_auth()
	# playlist: Playlist|None = requests.get_playlist(auth_token, "49PAThhKRCCTXeydvq9uAp")

	# card = Card(playlist.name, random_songs(playlist.songs))
	# card.save()


main()
