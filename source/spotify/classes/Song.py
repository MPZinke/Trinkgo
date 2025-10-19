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


from datetime import datetime, timedelta
import json
from typing import Optional


class Song:
	def __init__(
		self,
		id: int,
		uri: str,
		name: str,
		album: str,
		artists: str,
		artwork: str,
		length: int,
		playlist: Optional[object],
	):
		self.id: int = id
		self.uri: str = uri
		self.name: str = name
		self.album: str = album
		self.artists: str = artists
		self.artwork: str = artwork
		self.length: int = length
		self.playlist: Optional[object] = playlist


	def __iter__(self):
		yield from {
			"id": self.id,
			"uri": self.uri,
			"name": self.name,
			"album": self.album,
			"artists": self.artists,
			"artwork": self.artwork,
			"length": self.length,
			"playlist": self.playlist.id if(self.playlist is not None) else None,
		}.items()


	def __str__(self) -> str:
		return json.dumps(dict(self), indent=4)


	@staticmethod
	def from_dict(song_dict: dict):
		return Song(
			id=song_dict["id"],
			uri=song_dict["uri"],
			name=song_dict["name"],
			album=song_dict["album"],
			artists=song_dict["artists"],
			artwork=song_dict["artwork"],
			length=song_dict["length"],
			playlist=song_dict.get("playlist"),
		)

