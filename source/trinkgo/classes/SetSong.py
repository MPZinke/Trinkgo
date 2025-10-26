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


class SetSong:
	def __init__(
		self,
		id: int,
		start: int,
		duration: int,
		song: Song,
		playlist_set: Optional[object],
	):
		self.id: int = id
		self.start: int = start
		self.duration: int = duration
		self.song: Song = song
		self.playlist_set: Optional[object] = playlist_set


	def __eq__(self, right: object|None):
		return isinstance(right, SetSong) and self.id == right.id


	def __iter__(self):
		yield from {
			"id": self.id,
			"start": self.start,
			"duration": self.duration,
			"song": dict(self.song),
			"playlist_set": self.playlist_set.id if(self.playlist_set is not None) else None,
		}.items()


	def __str__(self) -> str:
		return json.dumps(dict(self), indent=4)


	@staticmethod
	def from_dict(**set_song_dict: dict):
		return SetSong(
			id=set_song_dict["id"],
			start=set_song_dict["start"],
			duration=set_song_dict["duration"],
			song=set_song_dict["song"],
			playlist_set=set_song_dict.get("playlist_set"),
		)
