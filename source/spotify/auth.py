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


import spotify


class LoginException(Exception):
	def __init__(self):
		super().__init__("Please login.")


class Tokens:
	def __init__(self):
		self._access_token: Optional[str] = None
		self._code: Optional[str] = None
		self._refresh_token: Optional[str] = None
		self.expiration: Optional[datetime] = None


	def __iter__(self) -> iter:
		yield from {
			"access_token": self._access_token,
			"code": self._code,
			"expiration": self.expiration if(self.expiration is not None) else None,
			"refresh_token": self._refresh_token,
		}.items()


	def __str__(self) -> str:
		return json.dumps(dict(self), default=str)


	@property
	def access_token(self) -> Optional[str]:
		if(self._code is None):
			return None
			# raise LoginException()

		if(self.expiration is None or self.expiration - timedelta(minutes=1) <= datetime.now()):
			auth_data: dict = spotify.requests.auth.refresh_access_token(self._refresh_token)
			self._access_token = auth_data.get("access_token")
			self.expiration = datetime.now() + timedelta(seconds=auth_data.get("expires_in"))

		return self._access_token


	@access_token.setter
	def access_token(self, access_token: str) -> None:
		self._access_token = access_token


	@property
	def authenticated(self) -> str:
		return self._code is not None


	@property
	def authorized(self) -> str:
		return self._access_token is not None


	@property
	def code(self) -> Optional[str]:
		return self._code


	@code.setter
	def code(self, code: str) -> None:
		auth_data: dict = spotify.requests.auth.get_access_token(code)
		self._code = code
		self._access_token = auth_data.get("access_token")
		self._refresh_token = auth_data.get("refresh_token")
		self.expiration = datetime.now() + timedelta(seconds=auth_data.get("expires_in"))


	def context_processor(self) -> dict:
		return {"access_token": self.access_token}
