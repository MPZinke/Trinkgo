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


from typing import Tuple


from PIL import Image, ImageDraw, ImageFont


from spotify.classes import Song


class Card:
	def __init__(self, name: str, songs: list[list[Song]]):
		self.name: str = name
		self.songs: list[Song] = [song_list.copy() for song_list in songs]

		self.width = 2480
		self.height = 3508
		self.image = Image.new("1", [self.width, self.height], 1)
		self.draw = ImageDraw.Draw(self.image)
		print(self.songs)  # TESTING


	@staticmethod
	def from_dict(card_dict: dict) -> object:
		...


	def save(self):
		square_size = 400
		half_square_size = square_size // 2

		self.center_text([square_size * 3, half_square_size], self.name, ImageFont.load_default(64))
		for x, row in enumerate(self.songs):
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
