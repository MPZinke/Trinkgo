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


from spotify.classes import Playlist, Song


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
