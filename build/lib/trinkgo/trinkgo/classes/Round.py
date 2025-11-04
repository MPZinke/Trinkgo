#!/opt/homebrew/bin/python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2025.10.11                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


from datetime import datetime
from typing import Optional, TypeVar


Card = TypeVar("Card")
Event = TypeVar("Event")
PlaylistSet = TypeVar("PlaylistSet")
SetSong = TypeVar("SetSong")


class Round:
	def __init__(
		self,
		id: int,
		name: str,
		size: list[int],
		start: Optional[datetime],
		ended: bool,
		cards: Optional[list[Card]],
		event: Optional[Event],
		played_set_songs: Optional[list[SetSong]],
		playlist_set: Optional[PlaylistSet],
	):
		self.id: int = id
		self.name: str = name
		self.size: list[int] = size
		self.start: datetime = start
		self.ended: bool = ended
		self.cards: Optional[list[Card]] = cards
		self.event: Optional[Event] = event
		self.played_set_songs: Optional[list[SetSong]] = played_set_songs
		self.playlist_set: Optional[PlaylistSet] = playlist_set


	@staticmethod
	def from_dict(**round_dict: dict):
		return Round(
			id=round_dict["id"],
			name=round_dict["name"],
			size=round_dict["size"],
			start=round_dict["start"],
			ended=round_dict["ended"],
			cards=round_dict.get("cards"),
			event=round_dict.get("event"),
			played_set_songs=round_dict.get("played_set_songs"),
			playlist_set=round_dict.get("playlist_set"),
		)
