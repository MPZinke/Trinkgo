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


class Round:
	def __init__(
		self,
		id: int,
		name: str,
		size: list[int],
		start: Optional[datetime],
		ended: bool,
		event: Optional[Event],
		playlist_set: Optional[PlaylistSet],
		cards: Optional[list[Card]],
	):
		self.id: int = id
		self.name: str = name
		self.size: list[int] = size
		self.start: datetime = start
		self.ended: bool = ended
		self.event: Optional[Event] = event
		self.playlist_set: Optional[PlaylistSet] = playlist_set
		self.cards: Optional[list[Card]] = cards


	@staticmethod
	def from_dict(**round_dict: dict):
		return Round(
			id=round_dict["id"],
			name=round_dict["name"],
			size=round_dict["size"],
			start=round_dict["start"],
			ended=round_dict["ended"],
			event=round_dict.get("event"),
			playlist_set=round_dict.get("playlist_set"),
			cards=round_dict.get("cards"),
		)
