#!/opt/homebrew/bin/python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2025.09.25                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


from datetime import datetime, timedelta
import json
from typing import Optional


class Tokens:
	def __init__(self):
		self.access_token: Optional[str] = None
		self.refresh_token: Optional[str] = None
		self._expiration: Optional[datetime] = None


	def __iter__(self) -> iter:
		yield from {
			"access_token": self.access_token,
			"expires_in": (self._expiration - datetime.now()).seconds,
			"refresh_token": self.refresh_token,
		}.items()


	def __str__(self) -> str:
		return json.dumps(dict(self))


	@property
	def expired(self) -> bool:
		if(self._expiration is None):
			return True

		return self._expiration - timedelta(minutes=1) <= datetime.now()


	def expires_in(self, seconds: int) -> None:
		self._expiration = datetime.now() + timedelta(seconds=seconds)


	expires_in = property(None, expires_in)



TOKENS = Tokens()
