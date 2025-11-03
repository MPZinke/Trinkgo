
from pathlib import Path
import random
from typing import Optional


from flask import request, Blueprint
from flask_login import current_user, login_required
from jinja2 import Environment, FileSystemLoader
import requests


import database
import spotify
from spotify.classes import Playlist, Song
from trinkgo.classes import Round, SetSong


WEBAPP_DIRECTORY = Path(__file__).parents[1]
HTML_DIRECTORY = WEBAPP_DIRECTORY / "html"
STATIC_DIRECTORY = WEBAPP_DIRECTORY / "static"


api_blueprint = Blueprint('api_blueprint', __name__, template_folder=HTML_DIRECTORY, static_folder=STATIC_DIRECTORY)


def render_template(template_path: str, **kwargs: dict) -> str:
	env = Environment(loader=FileSystemLoader(HTML_DIRECTORY))
	template = env.get_template(template_path)
	return template.render(**kwargs)


@api_blueprint.get("/api/play")
@login_required
def api_play():
	playlist = Playlist("49PAThhKRCCTXeydvq9uAp", "80's Stuff", [])
	spotify.requests.player.play_playlist(current_user, playlist)
	return ("", 204)


@api_blueprint.post("/api/songs/<int:id>/play")
@login_required
def api_song_play(id: int):
	request_json = request.json
	player_id: str = request_json["player_id"]

	song: Song = database.songs.select_song(id)

	spotify.requests.player.play_song(current_user, player_id, song)
	return ("", 204)


@api_blueprint.post("/api/set_songs/<int:id>/play")
@login_required
def api_set_songs_set_song_play(id: int):
	request_json = request.json
	player_id: str = request_json["player_id"]
	start: Optional[str] = request_json["start"]

	set_song: SetSong = database.set_songs.select_set_song(id)
	if(start is not None):
		set_song.start = int(start)

	spotify.requests.player.play_song(current_user, player_id, set_song.song, set_song.start)
	return ("", 204)


@api_blueprint.post("/api/set_songs/<int:id>/update")
@login_required
def api_set_song_set_songs_update(id: int):
	request_json = request.json
	label: int = request_json["label"]
	start: int = request_json["start"]
	duration: int = request_json["duration"]

	set_song = SetSong(
		id=id,
		label=label,
		start=start,
		duration=duration,
		song=None,  # Sacrilege, I know.
		playlist_set=None,
	)

	database.set_songs.update_set_song(set_song)

	return ("", 204)


@api_blueprint.post("/api/rounds/<int:id>/played_set_songs/new")
@login_required
def api_rounds_round_played_set_songs_new(id: int):
	request_json = request.json
	set_song_id: Optional[str]|int = request_json["set_song_id"]

	round: Round = database.rounds.select_round(id)
	database.events.select_event_for_round(round)
	database.playlist_sets.select_playlist_set_for_round(round)
	database.set_songs.select_set_songs_for_playlist_set(round.playlist_set)
	database.played_set_songs.select_played_set_songs_for_round(round)

	if(set_song_id is not None):
		set_song = next(filter(lambda set_song: set_song.id == set_song_id, round.playlist_set.set_songs))
	else:
		unplayed_set_songs = list(filter(lambda set_song: set_song not in round.played_set_songs, round.playlist_set.set_songs))
		set_song: SetSong = random.choice(unplayed_set_songs)

	database.played_set_songs.insert_played_set_song(set_song, round)

	return {
		"set_song_id": set_song.id,
		"duration": set_song.duration,
		"html": render_template(
			"events/event/rounds/round/play/_played_song.j2",
			index=len(round.played_set_songs),
			set_song=set_song
		)
	}


@api_blueprint.get("/api/next")
@login_required
def api_next():
	spotify.requests.player.play_next(current_user)
	return ("", 204)


@api_blueprint.post("/api/pause")
@login_required
def api_pause():
	player_id: str = request.json.get("player_id")
	spotify.requests.pause(current_user, player_id)
	return ("", 204)
