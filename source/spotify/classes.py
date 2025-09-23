

from datetime import datetime, timedelta
import json
from typing import Optional


class Song:
	def __init__(self, id: str, name: str, album: str, artists: str, artwork: str, start: int, duration: int):
		self.id: str = id
		self.name: str = name
		self.album: str = album
		self.artists: str = artists
		self.artwork: str = artwork
		self.start: int = start
		self.duration: int = duration


	def __iter__(self):
		yield from {
			"id": self.id,
			"name": self.name,
			"album": self.album,
			"artists": self.artists,
			"artwork": self.artwork,
			"start": self.start,
			"duration": self.duration,
		}.items()


	def __str__(self) -> str:
		return json.dumps(dict(self), indent=4)


	@staticmethod
	def from_dict(dictionary: dict):
		return Song(
			id=dictionary["id"],
			name=dictionary["name"],
			album=dictionary["album"],
			artists=dictionary["artists"],
			artwork=dictionary["artwork"],
			start=dictionary["start"],
			duration=dictionary["duration"],
		)


class Playlist:
	def __init__(self, id: str, name: str, songs: list[Song]):
		self.id: str = id
		self.name: str = name
		self.songs: list[Song] = songs.copy()


	def __iter__(self):
		yield from {
			"id": self.id,
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
		self._expiration: Optional[datetime] = None


	def __iter__(self) -> iter:
		yield from {
			"access_token": self.access_token,
			"device_id": self.device_id,
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
