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
		event: Event,
		playlist_set: PlaylistSet,
		cards: Optional[list[Card]],
	):
		self.id: int = id
		self.name: str = name
		self.size: list[int] = size
		self.start: datetime = start
		self.event: Event = event
		self.playlist_set: PlaylistSet = playlist_set
		self.cards: Optional[list[Card]] = cards


	@staticmethod
	def from_dict(round_dict: dict):
		return Round(
			id=round_dict["id"],
			name=round_dict["name"],
			size=round_dict["date"],
			start=round_dict["start"],
			event=round_dict.get("event"),
			playlist_set=round_dict["playlist_set"],
			cards=round_dict.get("cards"),
		)
