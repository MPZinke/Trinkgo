#!/opt/homebrew/bin/python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2025.06.01                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


from typing import Optional, Tuple, TypeVar


from PIL import Image, ImageDraw, ImageFont


from spotify.classes import Song
from trinkgo.classes import PlaylistSet, SetSong


Round = TypeVar("Round")


class CardSetSongs:
	def __init__(self, size: Tuple[int, int], set_songs: Optional[list[list[Optional[SetSong]]]]=None):  # ...Java?
		self.size = size

		if(set_songs is None):
			self.set_songs: list[list[None]] = [[None] * size[1] for _ in range(size[0])]
		else:
			self.set_songs: list[list[Optional[SetSong]]] = [set_songs_list.copy() for set_songs_list in self.set_songs]


	def __iter__(self) -> list:
		return iter(self.set_songs)


	def __getitem__(self, key: int|Tuple[int, int]) -> Optional[SetSong]|list[Optional[SetSong]]:
		if(isinstance(key, int)):
			return self.set_songs[key]

		return self.set_songs[key[0]][key[1]]


	def __setitem__(self, key: Tuple[int, int], value: Optional[SetSong]) -> None:
		self.set_songs[key[0]][key[1]] = value


	def copy(self):
		return CardSetSongs([0, 0], self.set_songs)


class Card:
	def __init__(
		self,
		id: int,
		identifier: int,
		size: Tuple[int, int],
		set_songs: CardSetSongs|list[list[SetSong]],
		round: Optional[Round]
	):
		if(not isinstance(set_songs, CardSetSongs)):
			set_songs = CardSetSongs(size, set_songs)

		self.id: int = id
		self.identifier: int = identifier
		self.size: Tuple[int, int] = size
		self.set_songs: CardSetSongs = set_songs
		self.round: Optional[Round] = round



		# self.name: str = name
		# self.set_songs: list[Song] = [song_list.copy() for song_list in set_songs]

		# self.width = 2480
		# self.height = 3508

		# print(self.set_songs)  # TESTING


	@staticmethod
	def from_dict(**card_dict: dict) -> object:
		return Card(
			id=card_dict["id"],
			identifier=card_dict["identifier"],
			size=card_dict["size"],
			set_songs=card_dict["set_songs"],
			round=card_dict.get("round"),
		)


	def pdf(self):
		def center_text(
			draw,
			center: Tuple[int, int],
			text: str,
			font: ImageFont=ImageFont.load_default(32),
			limit: int=None
		):
			text_width = draw.textlength(text, font=font)
			draw.text((center[0] - text_width//2, center[1] - font.size//2), text=text, font=font)

		width = 2480
		height = 3508
		margin = 50
		header_space = 300

		square_width = (width - (margin * 2)) // self.size[1]
		square_height = (height - header_space - (margin * 2)) // self.size[0]
		half_square_width = square_width // 2
		half_square_height = square_height // 2

		image = Image.new("1", [width, height], 1)
		draw = ImageDraw.Draw(image)

		header = f"{self.round.event.name} - {self.round.name} - {self.identifier}"
		center_text(draw, [width // 2, 82], header, ImageFont.load_default(64))
		for x, row in enumerate(self.set_songs):
			x_start = x * square_width + margin
			for y, set_song in enumerate(row):
				y_start = y * square_height + header_space + margin
				draw.rectangle([(x_start, y_start), (x_start+square_width, y_start+square_height)])
				text = "Free" if(set_song is None) else set_song.song.title
				center_text(draw, [x_start+half_square_width, y_start+half_square_height], text)

		image.save("/Users/mpzinke/Downloads/Test.jpg")
