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


def center_text(draw: ImageDraw.Draw, center: Tuple[int, int], text: str, font: ImageFont=ImageFont.load_default(32), limit: int=None):
	text_width = draw.textlength(text, font=font)
	draw.text((center[0] - text_width//2, center[1] - font.size//2), text=text, font=font)


class Card:
	def __init__(self, name: str, songs: list[Song]):
		self.name: str = name
		self.songs: list[Song] = [[songs[5 * x + y] for y in range(5)] for x in range(5)]
		print(self.songs)


	def save(self):
		square_size = 400
		half_square_size = square_size // 2
		height = width = square_size * 6

		image = Image.new("1", [width, height+half_square_size], 1)
		draw = ImageDraw.Draw(image)

		center_text(draw, [square_size * 3, half_square_size], self.name, ImageFont.load_default(64))
		for x, row in enumerate(self.songs):
			x = x * square_size + half_square_size
			for y, col in enumerate(row):
				y = (y+1) * square_size
				draw.rectangle([(x, y), (x+square_size, y+square_size)])
				center_text(draw, [x+half_square_size, y+half_square_size], col.name)

		image.save("/Users/mpzinke/Downloads/Test.jpg")
