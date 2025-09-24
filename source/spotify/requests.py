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


import requests


from spotify.classes import Playlist, Song, Player


def play_previous(player: Player):
	# FROM: https://developer.spotify.com/documentation/web-api/reference/skip-users-playback-to-previous-track
	url = f"https://api.spotify.com/v1/me/player/previous?device_id={player.device_id}"
	headers = {
		"Content-Type": "application/json",
		"Authorization": f"Bearer {player.access_token}"
	}
	response: requests.Response = requests.post(url, headers=headers)
	response.raise_for_status()
	return response.status_code != 204


def play_playlist(player: Player, playlist: Playlist):
	# FROM: https://developer.spotify.com/documentation/web-api/reference/start-a-users-playback
	#  AND: https://stackoverflow.com/questions/68047533/spotify-web-api-how-to-play-a-playlist
	url = f"https://api.spotify.com/v1/me/player/play?device_id={player.device_id}"
	headers = {
		"Content-Type": "application/json",
		"Authorization": f"Bearer {player.access_token}"
	}
	body = {"context_uri": f"spotify:playlist:{playlist.id}", "offset": {"position": 24}}
	response: requests.Response = requests.put(url, headers=headers, json=body)
	response.raise_for_status()
	return response.status_code != 204


def play_song(player: Player, player_id: str, song: Song):
	# FROM: https://developer.spotify.com/documentation/web-api/reference/start-a-users-playback
	url = f"https://api.spotify.com/v1/me/player/play?device_id={player_id}"
	headers = {
		"Content-Type": "application/json",
		"Authorization": f"Bearer {player.access_token}"
	}
	body = {"uris": [f"spotify:track:{song.id}"], "position_ms": song.start}
	response: requests.Response = requests.put(url, headers=headers, json=body)
	response.raise_for_status()
	return response.status_code != 204


def pause(player: Player, player_id: str):
	# FROM: https://developer.spotify.com/documentation/web-api/reference/pause-a-users-playback
	url = f"https://api.spotify.com/v1/me/player/pause?device_id={player_id}"
	headers = {
		"Content-Type": "application/json",
		"Authorization": f"Bearer {player.access_token}"
	}
	response: requests.Response = requests.put(url, headers=headers)
	response.raise_for_status()
	return response.status_code != 204


def play_next(player: Player):
	# FROM: https://developer.spotify.com/documentation/web-api/reference/skip-users-playback-to-next-track
	url = f"https://api.spotify.com/v1/me/player/next?device_id={player.device_id}"
	headers = {
		"Content-Type": "application/json",
		"Authorization": f"Bearer {player.access_token}"
	}
	response: requests.Response = requests.post(url, headers=headers)
	response.raise_for_status()
	return response.status_code != 204


def get_access_token(player: Player, code: str):
	# FROM: https://developer.spotify.com/documentation/web-playback-sdk/howtos/web-app-player
	#    @: Request Access Token
	url = "https://accounts.spotify.com/api/token"
	headers = {
		"Authorization": "Basic OGRjN2Y4Yjc1NzkzNGQ5ZWJhZjM5ZjkzNDdiY2NjNTY6N2U5YzQyMTI3OWI3NGQ2OWE2YTliNTBlNDkzY2ZhOGU=",
		"Content-Type": "application/x-www-form-urlencoded",
	}
	params = {
		"code": code,
		"grant_type": "authorization_code",
		"redirect_uri": "http://127.0.0.1:8080/authenticated",
	}
	response = requests.post(url, headers=headers, params=params)

	print(response.json())  # TEMP

	response_json = response.json()
	player.access_token = response_json.get("access_token")
	player.refresh_token = response_json.get("refresh_token")
	player.expires_in = response_json.get("expires_in")


def refresh_access_token(player: Player):
	# FROM: https://developer.spotify.com/documentation/web-api/tutorials/refreshing-tokens
	url = "https://accounts.spotify.com/api/token"
	headers = {
		"Content-Type": "application/x-www-form-urlencoded",
		"Authorization": "Basic OGRjN2Y4Yjc1NzkzNGQ5ZWJhZjM5ZjkzNDdiY2NjNTY6N2U5YzQyMTI3OWI3NGQ2OWE2YTliNTBlNDkzY2ZhOGU=",
	}
	params = {
		"grant_type": "refresh_token",
		"refresh_token": player.refresh_token,
	}
	response: requests.Response = requests.post(url, headers=headers, params=params)
	response.raise_for_status()

	response_json = response.json()
	player.access_token = response_json.get("access_token")
	player.expires_in = response_json.get("expires_in")


def get_playlist(player: Player, playlist_id: str) -> Playlist:
	url = (
		f"https://api.spotify.com/v1/playlists/{playlist_id}"
		"?fields=name,tracks.items(track(id,name,duration_ms,album.images,album.name,artists(name))"
	)
	headers = {"Authorization": f"Bearer {player.access_token}"}
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
			id=track["id"],
			name=track["name"],
			album=track["album"]["name"],
			artists=artists,
			artwork=artwork,
			start=0,
			duration=track["duration_ms"],
		)
		songs.append(song)

	return Playlist(playlist_id, playlist_info["name"], songs)
