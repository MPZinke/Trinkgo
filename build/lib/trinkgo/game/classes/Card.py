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


from io import BytesIO
from pathlib import Path
from typing import Optional, Tuple, TypeVar


from PIL import Image, ImageDraw, ImageFont


from trinkgo.spotify.classes import Song
from trinkgo.game.classes import PlaylistSet, SetSong


Round = TypeVar("Round")


class CardSetSongs:
	def __init__(self, size: Tuple[int, int], set_songs: Optional[list[list[Optional[SetSong]]]]=None):  # ...Java?
		self.size = size

		if(set_songs is None):
			self.set_songs: list[list[None]] = [[None] * size[1] for _ in range(size[0])]
		else:
			self.set_songs: list[list[Optional[SetSong]]] = [set_songs_list.copy() for set_songs_list in self.set_songs]


	def __eq__(self, right: object) -> bool:
		return self.set_songs == right.set_songs


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
	WIDTH = 2480
	HEIGHT = 3508
	MARGIN = 50
	HEADER_SPACE = 300


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
	def center_text(
		draw: ImageDraw.Draw,
		center: Tuple[int, int],
		text: str,
		font: ImageFont=ImageFont.load_default(40),
		limit: int=0
	):
		text_parts = []
		while(limit and text):
			text_width = draw.textlength(text, font=font)
			tokens = text.split(" ")
			for x in range(len(tokens)):  # Start at 0 to always iterate at least once.
				# Look ahead to second token, as we always want to consume at least 1 token to not infinitely loop.
				incremental_token = " ".join(tokens[:x+2])
				text_width = draw.textlength(incremental_token, font=font)
				if(text_width > limit):
					break

			text_parts.append(" ".join(tokens[:x+1]))
			text = " ".join(tokens[x+1:])
		else:
			text_parts.append(text)

		centering_offset = font.size//2
		for row, text_part in enumerate(text_parts):
			text_width = draw.textlength(text_part, font=font)
			y_offset = (row - len(text_parts) // 2) * font.size
			draw.text((center[0] - text_width//2, center[1]+y_offset-centering_offset), text=text_part, font=font)


	def image(self) -> Image:
		square_width = (self.WIDTH - (self.MARGIN * 2)) // self.size[1]
		square_height = (self.HEIGHT - self.HEADER_SPACE - (self.MARGIN * 2)) // self.size[0]
		half_square_width = square_width // 2
		half_square_height = square_height // 2

		image = Image.new("1", [self.WIDTH, self.HEIGHT], 1)
		draw = ImageDraw.Draw(image)

		header = f"{self.round.event.name} - {self.round.name} - {self.identifier}"
		logo = Image.open(Path(__file__).parents[2] / "webapp/static/images/logo_black.png").resize((150, 150))
		image.paste(logo, (self.WIDTH - self.MARGIN - 150, self.MARGIN), mask=logo)

		Card.center_text(draw, [self.WIDTH // 2, self.HEADER_SPACE / 2 + self.MARGIN], header, ImageFont.load_default(64))
		for y, row in enumerate(self.set_songs):
			y_start = y * square_height + self.HEADER_SPACE + self.MARGIN
			for x, set_song in enumerate(row):
				x_start = x * square_width + self.MARGIN
				draw.rectangle([(x_start, y_start), (x_start+square_width, y_start+square_height)])
				text = "Free" if(set_song is None) else set_song.song.title
				Card.center_text(draw, [x_start+half_square_width, y_start+half_square_height], text, limit=square_width-20)

		return image


	@staticmethod
	def pdf(card_images: Image.Image|list[Image]) -> BytesIO:
		if(isinstance(card_images, Image.Image)):
			card_images = [card_images]

		if(len(card_images) == 0):
			image = Image.new("1", [Card.WIDTH, Card.HEIGHT], 1)
			draw = ImageDraw.Draw(image)
			center = [Card.WIDTH // 2, Card.HEIGHT // 2]
			Card.center_text(draw, [center[0], center[1]-256], "Trinkgo by garum", ImageFont.load_default(256))
			Card.center_text(draw, center, "(There are currently no cards for this round)", ImageFont.load_default(64))
			card_images.append(image)

		# FROM: https://stackoverflow.com/a/10170635
		#  AND: https://stackoverflow.com/a/74204854
		pdf = BytesIO()
		card_images[0].save(pdf, "PDF", save_all=True, append_images=card_images[1:])
		pdf.seek(0)
		return pdf
