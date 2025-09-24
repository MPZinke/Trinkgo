

import psycopg2.extras


from database.connect import connect
from spotify.classes import Song


@connect
def select_song(cursor: psycopg2.extras.RealDictCursor, id: str) -> Song:
	query = """SELECT * FROM "Songs" WHERE "id" = %s AND "is_deleted" = FALSE;"""
	cursor.execute(query, (id,))
	playlist_dict = cursor.fetchone()

	return Song.from_dict(playlist_dict)
