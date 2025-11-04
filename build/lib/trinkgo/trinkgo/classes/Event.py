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


from datetime import date as date_type, datetime
from typing import Optional, TypeVar


Round = TypeVar("Round")


class Event:
	def __init__(
		self,
		id: int,
		name: str,
		date: date_type,
		start: Optional[datetime],
		ended: bool,
		rounds: Optional[list[Round]]=None
	):
		self.id: int = id
		self.name: str = name
		self.date: date_type = date
		self.start: datetime = start
		self.ended: bool = ended
		self.rounds: Optional[list[Round]] = rounds


	@staticmethod
	def from_dict(**event_dict: dict):
		return Event(
			id=event_dict["id"],
			name=event_dict["name"],
			date=event_dict["date"],
			start=event_dict["start"],
			ended=event_dict["ended"],
			rounds=event_dict.get("rounds"),
		)
