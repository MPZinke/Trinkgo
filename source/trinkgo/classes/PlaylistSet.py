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


from spotify.classes import Playlist, Song
from trinkgo.classes import SetSong


class PlaylistSet:
	def __init__(self, id: int, name: str, playlist: Optional[Playlist], songs: list[SetSong]|None):
		self.id: int = id
		self.name: str = name
		self.playlist: Optional[Playlist] = playlist
		self.songs: list[SetSong]|None = songs.copy() if(songs is not None) else None


	def __iter__(self):
		yield from {
			"id": self.id,
			"name": self.name,
			"playlist": self.playlist if(self.playlist is not None) else None,
			"songs": list(map(dict, self.songs)) if(self.songs is not None) else None,
		}.items()


	def __str__(self) -> str:
		return json.dumps(dict(self), indent=4)


	@staticmethod
	def from_dict(playlist_set_dict: dict):
		return PlaylistSet(
			id=playlist_set_dict["id"],
			name=playlist_set_dict["name"],
			playlist=Playlist(
				id=playlist_set_dict["Playlists.id"],
				name=playlist_set_dict["Playlists.name"],
				uri=playlist_set_dict["Playlists.name"],
				songs=[],
			),
			songs=playlist_set_dict.get("songs")
		)
