#!/opt/homebrew/bin/python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2025.10.06                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


import json
from typing import Optional


from spotify.classes import Playlist
from trinkgo.classes import SetSong


class PlaylistSet:
	def __init__(self, id: int, name: str, playlist: Playlist, set_songs: list[SetSong]):
		self.id: int = id
		self.name: str = name
		self.playlist: Playlist = playlist
		self.set_songs: list[SetSong] = set_songs.copy() if(set_songs is not None) else None


	def __iter__(self):
		yield from {
			"id": self.id,
			"name": self.name,
			"playlist": dict(self.playlist) if(self.playlist is not None) else None,
			"set_songs": list(map(dict, self.set_songs)) if(self.set_songs is not None) else None,
		}.items()


	def __str__(self) -> str:
		return json.dumps(dict(self), indent=4)


	@staticmethod
	def from_dict(**playlist_set_dict: dict):
		return PlaylistSet(
			id=playlist_set_dict["id"],
			name=playlist_set_dict["name"],
			playlist=playlist_set_dict.get("playlist"),
			set_songs=playlist_set_dict.get("set_songs")
		)
