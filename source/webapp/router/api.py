
from pathlib import Path
from time import sleep  # TESTING
from typing import Optional


from flask import request, Blueprint
from jinja2 import Environment, FileSystemLoader
import requests


import database
import spotify
from spotify.classes import Playlist, Song
from trinkgo.classes import Round, SetSong
from webapp.router import app
from webapp.router.auth import authorize


WEBAPP_DIRECTORY = Path(__file__).parents[1]
HTML_DIRECTORY = WEBAPP_DIRECTORY / "html"
STATIC_DIRECTORY = WEBAPP_DIRECTORY / "static"


api_blueprint = Blueprint('api_blueprint', __name__, template_folder=HTML_DIRECTORY, static_folder=STATIC_DIRECTORY)


def render_template(template_path: str, **kwargs: dict) -> str:
	env = Environment(loader = FileSystemLoader(HTML_DIRECTORY))
	template = env.get_template(template_path)
	return template.render(**kwargs)


@api_blueprint.get("/api/play")
@authorize
def api_play():
	# song = Song("7zLGHdfJ3JRPxvc96mEPEi", "Out Of Touch", 0)
	# spotify.requests.player.play_song(TOKENS, song)
	playlist = Playlist("49PAThhKRCCTXeydvq9uAp", "80's Stuff", [])
	spotify.requests.player.play_playlist(app.tokens, playlist)
	return ("", 204)


@api_blueprint.post("/api/song/play")
@authorize
def api_song_play():
	request_json = request.json
	print(request_json)
	player_id: str = request_json.get("player_id")
	id: str = request_json.get("id")

	song: Song = database.song.select_song(id)

	spotify.requests.player.play_song(app.tokens, player_id, song)
	return ("", 204)


@api_blueprint.post("/api/set_song/play")
@authorize
def api_set_song_play():
	request_json = request.json
	player_id: str = request_json.get("player_id")
	id: str = request_json.get("id")
	start: str = request_json.get("start")

	set_song: SetSong = database.set_song.select_set_song(id)
	if(isinstance(start, str) and start.isnumeric()):
		set_song.start = int(start)

	spotify.requests.player.play_song(app.tokens, player_id, set_song.song, set_song.start)
	return ("", 204)


@api_blueprint.post("/api/set_song/update_start_and_duration")
@authorize
def api_song_save():
	request_json = request.json
	set_song_id: str = request_json.get("set_song_id")
	start: int = request_json.get("start")
	duration: int = request_json.get("duration")

	set_song = SetSong(
		id=set_song_id,
		start=start,
		duration=duration,
		song=None,  # Sacrilege, I know.
		playlist_set=None,
	)

	database.set_song.update_song_start_and_duration(set_song)

	return ("", 204)


@api_blueprint.post("/api/rounds/<int:round_id>/played_set_songs/new")
@authorize
def api_rounds_round_play_next(round_id: int):
	request_json = request.json
	player_id: str = request_json.get("player_id")
	set_song_id: int = int(request_json.get("set_song_id"))

	round: Round = database.round.select_round(round_id)
	database.event.select_event_for_round(round)
	database.playlist_set.select_playlist_set_for_round(round)
	database.set_song.select_set_songs_for_playlist_set(round.playlist_set)
	database.played_set_song.select_played_set_songs_for_round(round)

	set_song = next(filter(lambda set_song: set_song.id == set_song_id, round.playlist_set.set_songs))
	database.played_set_song.insert_played_set_song(set_song, round)

	return {
		"duration": set_song.duration,
		"html": render_template(
			"events/event/rounds/round/play/_played_song.j2",
			index=len(round.played_set_songs),
			set_song=set_song
		)
	}


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
