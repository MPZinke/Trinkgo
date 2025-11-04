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
import traceback
from typing import Optional


import flask_login


from trinkgo import spotify


class LoginException(Exception):
	def __init__(self):
		super().__init__("Please login.")


class SpotifyUserAuth:
	def __init__(
		self,
		access_token: str=None,
		code: str=None,
		expiration: datetime=None,
		refresh_token: str=None,
	):
		self._access_token: str = access_token
		self._code: str = code
		self._expiration: datetime = expiration
		self._refresh_token: str = refresh_token


	@property
	def access_token(self) -> Optional[str]:
		if(self._code is None):
			return None

		if(self._expiration is None or self._expiration - timedelta(minutes=1) <= datetime.now()):
			auth_data: dict = spotify.requests.auth.refresh_access_token(self._refresh_token)
			self._access_token = auth_data.get("access_token")
			self._expiration = datetime.now() + timedelta(seconds=auth_data.get("expires_in"))
			flask_login.login_user(self)

		return self._access_token


	@property
	def is_authenticated(self):
		if(self._code is None):
			return False

		if(datetime.now() < self._expiration - timedelta(minutes=1)):
			return True

		try:
			auth_data: dict = spotify.requests.auth.refresh_access_token(self._refresh_token)
			self._access_token = auth_data.get("access_token")
			self._expiration = datetime.now() + timedelta(seconds=auth_data.get("expires_in"))
			flask_login.login_user(self)
			return True

		except Exception:
			traceback.print_exc()
			return False


	@property
	def is_active(self):
		return True


	@property
	def is_anonymous(self):
		return False


	def get_id(self):
		return json.dumps(
			{
				"access_token": self._access_token,
				"code": self._code,
				"expiration": self._expiration,
				"refresh_token": self._refresh_token,
			},
			default=str,
		)
