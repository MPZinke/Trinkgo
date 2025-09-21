

import json
from typing import Optional


class Song:
	def __init__(self, id: str, name: str, position: str):
		self.id: str = id
		self.name: str = name
		self.position: int = position


	def __iter__(self):
		yield from {
			"id": self.id,
			"name": self.name,
			"position": self.position,
		}.items()


	def __str__(self) -> str:
		return json.dumps(dict(self), indent=4)


class Playlist:
	def __init__(self, id: str, name: str, songs: list[Song]):
		self.id: str = id
		self.name: str = name
		self.songs: list[Song] = songs.copy()


	def __iter__(self):
		yield from {
			"name": self.name,
			"songs": list(map(dict, self.songs)),
		}.items()


	def __str__(self) -> str:
		return json.dumps(dict(self), indent=4)


class Player:
	def __init__(self):
		self.access_token: Optional[str] = None
		self.device_id: Optional[str] = None
		self.refresh_token: Optional[str] = None


	def __iter__(self) -> iter:
		yield from {
			"access_token": self.access_token,
			"device_id": self.device_id,
			"refresh_token": self.refresh_token,
		}.items()


	def __str__(self) -> str:
		return json.dumps(dict(self))

