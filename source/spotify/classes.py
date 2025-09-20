

import json


class Song:
	def __init__(self, name: str, href: str):
		self.name: str = name
		self.href: str = href


	def __iter__(self):
		yield from {
			"name": self.name,
			"href": self.href,
		}.items()


	def __str__(self) -> str:
		return json.dumps(dict(self), indent=4)


class Playlist:
	def __init__(self, name: str, songs: list[Song]):
		self.name: str = name
		self.songs: list[Song] = songs.copy()


	def __iter__(self):
		yield from {
			"name": self.name,
			"songs": list(map(dict, self.songs)),
		}.items()


	def __str__(self) -> str:
		return json.dumps(dict(self), indent=4)
