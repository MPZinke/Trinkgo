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


from spotify.classes import Song


class Playlist:
	def __init__(self, id: int, uri: str, title: str, songs: list[Song]):
		self.id: int = id
		self.uri: str = uri
		self.title: str = title
		self.songs: list[Song] = songs.copy() if(songs is not None) else None


	def __iter__(self):
		yield from {
			"id": self.id,
			"uri": self.uri,
			"title": self.title,
			"songs": list(map(dict, self.songs)) if(self.songs is not None) else None,
		}.items()


	def __str__(self) -> str:
		return json.dumps(dict(self), indent=4)


	@staticmethod
	def from_dict(**playlist_dict: dict):
		return Playlist(
			id=playlist_dict["id"],
			uri=playlist_dict["uri"],
			title=playlist_dict["title"],
			songs=playlist_dict.get("songs")
		)
