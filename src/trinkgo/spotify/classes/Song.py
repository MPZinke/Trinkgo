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


from datetime import date as date_type, datetime, timedelta
import json
from typing import Optional


class Song:
	def __init__(
		self,
		id: int,
		uri: str,
		title: str,
		album: str,
		artists: str,
		artwork: str,
		length: int,
		released: date_type,
		playlist: Optional[object],
	):
		self.id: int = id
		self.uri: str = uri
		self.title: str = title
		self.album: str = album
		self.artists: str = artists
		self.artwork: str = artwork
		self.length: int = length
		self.released: date_type = released
		self.playlist: Optional[object] = playlist


	def __iter__(self):
		yield from {
			"id": self.id,
			"uri": self.uri,
			"title": self.title,
			"album": self.album,
			"artists": self.artists,
			"artwork": self.artwork,
			"length": self.length,
			"released": self.released,
			"playlist": self.playlist.id if(self.playlist is not None) else None,
		}.items()


	def __str__(self) -> str:
		return json.dumps(dict(self), indent=4)


	@staticmethod
	def from_dict(**song_dict: dict):
		return Song(
			id=song_dict["id"],
			uri=song_dict["uri"],
			title=song_dict["title"],
			album=song_dict["album"],
			artists=song_dict["artists"],
			artwork=song_dict["artwork"],
			length=song_dict["length"],
			released=song_dict["released"],
			playlist=song_dict.get("playlist"),
		)

