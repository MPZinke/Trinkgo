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


from trinkgo.spotify.auth import SpotifyUserAuth
from trinkgo.spotify.classes import Playlist, Song


def play_previous(tokens: SpotifyUserAuth, player_id: str):
	# FROM: https://developer.spotify.com/documentation/web-api/reference/skip-users-playback-to-previous-track
	url = f"https://api.spotify.com/v1/me/player/previous?device_id={player_id}"
	headers = {
		"Content-Type": "application/json",
		"Authorization": f"Bearer {tokens.access_token}"
	}
	response: requests.Response = requests.post(url, headers=headers)
	response.raise_for_status()
	return response.status_code != 204


def play_playlist(tokens: SpotifyUserAuth, player_id: str, playlist: Playlist):
	# FROM: https://developer.spotify.com/documentation/web-api/reference/start-a-users-playback
	#  AND: https://stackoverflow.com/questions/68047533/spotify-web-api-how-to-play-a-playlist
	url = f"https://api.spotify.com/v1/me/player/play?device_id={player_id}"
	headers = {
		"Content-Type": "application/json",
		"Authorization": f"Bearer {tokens.access_token}"
	}
	body = {"context_uri": f"spotify:playlist:{playlist.id}", "offset": {"position": 24}}
	response: requests.Response = requests.put(url, headers=headers, json=body)
	response.raise_for_status()
	return response.status_code != 204


def play_song(tokens: SpotifyUserAuth, player_id: str, song: Song, start: int=0):
	# FROM: https://developer.spotify.com/documentation/web-api/reference/start-a-users-playback
	url = f"https://api.spotify.com/v1/me/player/play?device_id={player_id}"
	headers = {
		"Content-Type": "application/json",
		"Authorization": f"Bearer {tokens.access_token}"
	}
	body = {"uris": [f"spotify:track:{song.uri}"], "position_ms": start}
	response: requests.Response = requests.put(url, headers=headers, json=body)
	response.raise_for_status()
	return response.status_code != 204


def pause(tokens: SpotifyUserAuth, player_id: str):
	# FROM: https://developer.spotify.com/documentation/web-api/reference/pause-a-users-playback
	url = f"https://api.spotify.com/v1/me/player/pause?device_id={player_id}"
	headers = {
		"Content-Type": "application/json",
		"Authorization": f"Bearer {tokens.access_token}"
	}
	response: requests.Response = requests.put(url, headers=headers)
	response.raise_for_status()
	return response.status_code != 204


def play_next(tokens: SpotifyUserAuth, player_id: str):
	# FROM: https://developer.spotify.com/documentation/web-api/reference/skip-users-playback-to-next-track
	url = f"https://api.spotify.com/v1/me/player/next?device_id={player_id}"
	headers = {
		"Content-Type": "application/json",
		"Authorization": f"Bearer {tokens.access_token}"
	}
	response: requests.Response = requests.post(url, headers=headers)
	response.raise_for_status()
	return response.status_code != 204



def get_playlist(tokens: SpotifyUserAuth, playlist_id: str) -> Playlist:
	url = (
		f"https://api.spotify.com/v1/playlists/{playlist_id}"
		"?fields=name,tracks.items(track(id,name,duration_ms,album.images,album.name,artists(name))"
	)
	headers = {"Authorization": f"Bearer {tokens.access_token}"}
	response: requests.Response = requests.get(url, headers=headers)
	response.raise_for_status()

	playlist_info = response.json()
	songs = []
	for song_info in playlist_info["tracks"]["items"]:
		track = song_info["track"]

		artists = ", ".join(artist["name"] for artist in track["artists"])

		images: list[dict] = track["album"]["images"]
		images.sort(key=lambda image: image["width"])
		artwork = next((image["url"] for image in images), None)

		song = Song(
			playlist_id=playlist_id,
			id=track["id"],
			name=track["name"],
			album=track["album"]["name"],
			artists=artists,
			artwork=artwork,
			start=0,
			length=track["duration_ms"],
		)
		songs.append(song)

	return Playlist(playlist_id, playlist_info["name"], songs)
