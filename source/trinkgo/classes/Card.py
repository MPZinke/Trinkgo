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
		return self.set_songs


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
		# self.image = Image.new("1", [self.width, self.height], 1)
		# self.draw = ImageDraw.Draw(self.image)
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


	@staticmethod
	def new(round: Round, number_of_boards: int) -> list[object]:
		for x in range(number_of_boards):
			...


	def save(self):
		square_size = 400
		half_square_size = square_size // 2

		self.center_text([square_size * 3, half_square_size], self.round.name, ImageFont.load_default(64))
		for x, row in enumerate(self.set_set_songs):
			x = x * square_size + half_square_size
			for y, col in enumerate(row):
				y = (y+1) * square_size
				self.draw.rectangle([(x, y), (x+square_size, y+square_size)])
				self.center_text([x+half_square_size, y+half_square_size], col.name)

		self.image.save("/Users/mpzinke/Downloads/Test.jpg")


	def center_text(
		self,
		center: Tuple[int, int],
		text: str,
		font: ImageFont=ImageFont.load_default(32),
		limit: int=None
	):
		text_width = self.draw.textlength(text, font=font)
		self.draw.text((center[0] - text_width//2, center[1] - font.size//2), text=text, font=font)
