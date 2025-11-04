

import os
import psycopg2
import psycopg2.extras



def connect(function: callable) -> callable:
	"""
	SUMMARY: Wraps a DB function with calls to connect and closes the DB.
	PARAMS:  Takes the function that will be wrapped.
	RETURNS: The function pointer that wraps the function.
	"""
	def wrapper(*args: list, **kwargs: dict) -> list|dict:
		"""
		DETAILS: Creates a connection and passes it to the calling function.
		RETURNS: Value(s) if values.
		THROWS:  Whatever exceptions occur during function call.
		"""
		DB_host: str = os.getenv("DB_HOST", "localhost")
		DB_user: str = os.getenv("DB_USER", "trinkgo")
		DB_password: str = os.getenv("DB_PASSWORD", "")

		connection_string = f"host={DB_host} dbname=Trinkgo user={DB_user} password={DB_password}"
		with psycopg2.connect(connection_string) as connection:
			connection.autocommit = True  # Automatically commit changes to DB
			with connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
				results: list|dict = function(cursor, *args, **kwargs)

				return results

	wrapper.__name__ = function.__name__
	return wrapper
