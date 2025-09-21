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


def pause(player: Player):
	# FROM: https://developer.spotify.com/documentation/web-api/reference/pause-a-users-playback
	url = f"https://api.spotify.com/v1/me/player/pause?device_id={player.device_id}"
	headers = {
		"Content-Type": "application/json",
		"Authorization": f"Bearer {player.access_token}"
	}
	response: requests.Response = requests.put(url, headers=headers)
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
	body = {"context_uri": f"spotify:playlist:{playlist.id}"}
	response: requests.Response = requests.put(url, headers=headers, json=body)
	return response.status_code != 204


def play_song(player: Player, song: Song):
	# FROM: https://developer.spotify.com/documentation/web-api/reference/start-a-users-playback
	url = f"https://api.spotify.com/v1/me/player/play?device_id={player.device_id}"
	headers = {
		"Content-Type": "application/json",
		"Authorization": f"Bearer {player.access_token}"
	}
	body = {"uris": [f"spotify:track:{song.id}"], "position_ms": song.position}
	# body = {"context_uri": f"spotify:track:{song.id}"}
	response: requests.Response = requests.put(url, headers=headers, json=body)
	return response.status_code != 204


def refresh_access_token(refresh_token: str):
	# FROM: https://developer.spotify.com/documentation/web-api/tutorials/refreshing-tokens
	url = "https://accounts.spotify.com/api/token"
	headers = {"Content-Type": "application/x-www-form-urlencoded"}
	params = {
		"refresh_token": refresh_token,
		"grant_type": "refresh_token",
		"client_id": "8dc7f8b757934d9ebaf39f9347bccc56",
	}
	response: requests.Response = requests.post(url, headers=headers, params=params)
	if(response.status_code != 200):
		return None, None

	return response.json().get("access_token"), response.json().get("refresh_token")


def get_auth() -> str:
	url = "https://accounts.spotify.com/api/token"
	data = "grant_type=client_credentials&client_id=56e541fab6734e6090619912859410ac&client_secret=e273d962b1504139af9a520e8532a539"
	headers = {"Content-Type": "application/x-www-form-urlencoded"}
	response: requests.Response = requests.post(url, headers=headers, data=data)
	response.raise_for_status()

	return response.json().get("access_token")


def get_playlist(auth_token: str, playlist_id: str) -> dict|None:
	url = f"https://api.spotify.com/v1/playlists/{playlist_id}?fields=name,tracks.items(track(name,href))"
	headers = {"Authorization": f"Bearer {auth_token}"}
	response: requests.Response = requests.get(url, headers=headers)

	if(response.status_code == 401):
		return None
	response.raise_for_status()

	playlist_info = response.json()
	songs = []
	for song_info in playlist_info["tracks"]["items"]:
		songs.append(Song(song_info["track"]["name"], song_info["track"]["href"]))

	return Playlist(playlist_info["name"], songs)
