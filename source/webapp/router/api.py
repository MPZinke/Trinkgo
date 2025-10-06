
import os
from pathlib import Path
from typing import Optional


from flask import request, Blueprint
import requests


import database
import spotify
from spotify.classes import Playlist, Song
from webapp.router import app
from webapp.router.auth import authorize


WEBAPP_DIRECTORY = Path(__file__).parents[1]
HTML_DIRECTORY = WEBAPP_DIRECTORY / "html"
STATIC_DIRECTORY = WEBAPP_DIRECTORY / "static"


api_blueprint = Blueprint('api_blueprint', __name__, template_folder=HTML_DIRECTORY, static_folder=STATIC_DIRECTORY)


@api_blueprint.get("/api/play")
@authorize
def api_play():
	# song = Song("7zLGHdfJ3JRPxvc96mEPEi", "Out Of Touch", 0)
	# spotify.requests.player.play_song(TOKENS, song)
	playlist = Playlist("49PAThhKRCCTXeydvq9uAp", "80's Stuff", [])
	spotify.requests.player.play_playlist(app.tokens, playlist)
	return ("", 204)


@api_blueprint.post("/api/play/song")
@authorize
def api_play_song():
	request_json = request.json
	print(request_json)
	player_id: str = request_json.get("player_id")
	uri: str = request_json.get("uri")
	start: Optional[int] = request_json.get("start", 0)

	song = Song(
		id=0,
		uri=uri,
		name=None,
		album=None,
		artists=None,
		artwork=None,
		length=None,
		playlist=None,
	)

	spotify.requests.player.play_song(app.tokens, player_id, song, start)
	return ("", 204)


@api_blueprint.post("/api/song/save")
@authorize
def api_song_save():
	request_json = request.json
	playlist_id: str = request_json.get("playlist_id")
	song_id: str = request_json.get("song_id")
	start: int = request_json.get("start")
	duration: int = request_json.get("duration")

	database.song.update_song_start_and_duration(song_id, start, duration)

	return ("", 204)


@api_blueprint.get("/api/next")
@authorize
def api_next():
	spotify.requests.player.play_next(app.tokens)
	return ("", 204)


@api_blueprint.post("/api/pause")
@authorize
def api_pause():
	player_id: str = request.json.get("player_id")
	spotify.requests.pause(app.tokens, player_id)
	return ("", 204)
