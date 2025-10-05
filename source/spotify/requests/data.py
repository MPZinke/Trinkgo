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


import requests


from spotify.auth import Tokens
from spotify.classes import Playlist, Song


def get_playlist(tokens: Tokens, uri: str) -> Playlist:
	url = (
		f"https://api.spotify.com/v1/playlists/{uri}"
		"?fields=name,tracks.items(track(id,name,duration_ms,album.images,album.name,artists(name))"
	)
	headers = {"Authorization": f"Bearer {tokens.access_token}"}
	response: requests.Response = requests.get(url, headers=headers)
	response.raise_for_status()

	playlist_info = response.json()

	playlist = Playlist(id=0, uri=uri, name=playlist_info["name"], songs=[])
	for song_info in playlist_info["tracks"]["items"]:
		track = song_info["track"]

		artists = ", ".join(artist["name"] for artist in track["artists"])

		images: list[dict] = track["album"]["images"]
		images.sort(key=lambda image: image["width"])
		artwork = next((image["url"] for image in images), None)

		song = Song(
			id=0,
			uri=track["id"],
			name=track["name"],
			album=track["album"]["name"],
			artists=artists,
			artwork=artwork,
			length=track["duration_ms"],
			playlist=playlist,
		)
		playlist.songs.append(song)

	return playlist
