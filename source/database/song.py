

import psycopg2.extras


from database.connect import connect
from spotify.classes import Playlist, Song


@connect
def select_song(cursor: psycopg2.extras.RealDictCursor, playlist_id: str, id: str) -> Song:
	query = """SELECT * FROM "Songs" WHERE "Playlists.id" = %s AND "id" = %s AND "is_deleted" = FALSE;"""
	cursor.execute(query, (playlist_id, id))
	song_dict = cursor.fetchone()

	return Song.from_dict(**song_dict)


@connect
def select_songs_for_playlist(cursor: psycopg2.extras.RealDictCursor, playlist: Playlist) -> None:
	query = """SELECT * FROM "Songs" WHERE "Playlists.id" = %s AND "is_deleted" = FALSE;"""
	cursor.execute(query, (playlist.id,))
	playlist.songs = [Song.from_dict(playlist=playlist, **song_dict) for song_dict in cursor]


@connect
def update_song_start_and_duration(
	cursor: psycopg2.extras.RealDictCursor,
	id: str,
	start: int,
	duration: int
) -> Song:
	query = """
		UPDATE "SongsSets"
		SET "start" = %s, "duration" = %s
		WHERE "id" = %s
		  AND "is_deleted" = FALSE
		RETURNING *;
	"""
	cursor.execute(query, (start, duration, id))

	return dict(cursor.fetchone())