

import psycopg2.extras


from database.connect import connect
from spotify.classes import Playlist, Song


@connect
def select_song(cursor: psycopg2.extras.RealDictCursor, id: str) -> Song:
	query = """SELECT * FROM "Songs" WHERE "id" = %s AND "is_deleted" = FALSE;"""
	cursor.execute(query, (id,))
	song_dict = cursor.fetchone()

	return Song.from_dict(**song_dict)


@connect
def select_songs_for_playlist(cursor: psycopg2.extras.RealDictCursor, playlist: Playlist) -> None:
	query = """SELECT * FROM "Songs" WHERE "Playlists.id" = %s AND "is_deleted" = FALSE;"""
	cursor.execute(query, (playlist.id,))
	playlist.songs = [Song.from_dict(playlist=playlist, **song_dict) for song_dict in cursor]
