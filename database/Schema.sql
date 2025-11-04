

DROP TABLE IF EXISTS "Playlists" CASCADE;
CREATE TABLE "Playlists"
(
	"id" SERIAL NOT NULL PRIMARY KEY,
	"uri" CHAR(22) NOT NULL,
	"title" TEXT NOT NULL,
	"is_deleted" BOOL NOT NULL DEFAULT FALSE
);


DROP TABLE IF EXISTS "Songs" CASCADE;
CREATE TABLE "Songs"
(
	"id" SERIAL NOT NULL PRIMARY KEY,
	"uri" CHAR(22) NOT NULL,
	"title" TEXT NOT NULL,
	"album" TEXT NOT NULL,
	"artists" TEXT NOT NULL,
	"artwork" TEXT DEFAULT NULL,
	"length" INT NOT NULL DEFAULT 0,
	"released" VARCHAR(10) NOT NULL,
	"is_deleted" BOOL NOT NULL DEFAULT FALSE,
	"Playlists.id" INT NOT NULL,
	FOREIGN KEY ("Playlists.id") REFERENCES "Playlists" ("id")
);


DROP TABLE IF EXISTS "PlaylistsSets" CASCADE;
CREATE TABLE "PlaylistsSets"
(
	"id" SERIAL NOT NULL PRIMARY KEY,
	"name" TEXT NOT NULL UNIQUE,
	"is_deleted" BOOL NOT NULL DEFAULT FALSE,
	"Playlists.id" INT NOT NULL,
	FOREIGN KEY ("Playlists.id") REFERENCES "Playlists" ("id")
);


DROP TABLE IF EXISTS "SongsSets" CASCADE;
CREATE TABLE "SongsSets"
(
	"id" SERIAL NOT NULL PRIMARY KEY,
	"label" TEXT NOT NULL,
	"start" INT NOT NULL DEFAULT 0,
	"duration" INT NOT NULL DEFAULT 0,
	"is_deleted" BOOL NOT NULL DEFAULT FALSE,
	"Songs.id" INT NOT NULL,
	"PlaylistsSets.id" INT NOT NULL,
	FOREIGN KEY ("Songs.id") REFERENCES "Songs" ("id"),
	FOREIGN KEY ("PlaylistsSets.id") REFERENCES "PlaylistsSets" ("id")
);


DROP TABLE IF EXISTS "Events" CASCADE;
CREATE TABLE "Events"
(
	"id" SERIAL NOT NULL PRIMARY KEY,
	"name" TEXT NOT NULL,
	"date" DATE NOT NULL DEFAULT CURRENT_TIMESTAMP,
	"start" TIMESTAMP DEFAULT NULL,
	"ended" BOOLEAN DEFAULT FALSE,
	"is_deleted" BOOL NOT NULL DEFAULT FALSE,
	UNIQUE ("name", "date")
);


DROP TABLE IF EXISTS "Rounds" CASCADE;
CREATE TABLE "Rounds"
(
	"id" SERIAL NOT NULL PRIMARY KEY,
	"name" TEXT NOT NULL,
	"size" INT[2] NOT NULL DEFAULT ARRAY[5, 5]::INT[2],
	"start" TIMESTAMP DEFAULT NULL,
	"ended" BOOLEAN DEFAULT FALSE,
	"is_deleted" BOOL NOT NULL DEFAULT FALSE,
	"Events.id" INT NOT NULL,
	"PlaylistsSets.id" INT NOT NULL,
	FOREIGN KEY ("Events.id") REFERENCES "Events" ("id"),
	FOREIGN KEY ("PlaylistsSets.id") REFERENCES "PlaylistsSets" ("id")
);


DROP TABLE IF EXISTS "PlayedSongsSets" CASCADE;
CREATE TABLE "PlayedSongsSets"
(
	"id" SERIAL NOT NULL PRIMARY KEY,
	"played_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	"Rounds.id" INT NOT NULL,
	"SongsSets.id" INT NOT NULL,
	FOREIGN KEY ("Rounds.id") REFERENCES "Rounds" ("id"),
	FOREIGN KEY ("SongsSets.id") REFERENCES "SongsSets" ("id"),
	UNIQUE ("Rounds.id", "SongsSets.id")
);


DROP TABLE IF EXISTS "Cards" CASCADE;
CREATE TABLE "Cards"
(
	"id" SERIAL NOT NULL PRIMARY KEY,
	"identifier" VARCHAR(4) NOT NULL,
	"size" INT[2] NOT NULL DEFAULT ARRAY[5, 5]::INT[2],
	"PlayedSongsSets.id" INT DEFAULT NULL,
	"Rounds.id" INT NOT NULL,
	"is_deleted" BOOL NOT NULL DEFAULT FALSE,
	FOREIGN KEY ("PlayedSongsSets.id") REFERENCES "PlayedSongsSets" ("id"),
	FOREIGN KEY ("Rounds.id") REFERENCES "Rounds" ("id"),
	UNIQUE ("identifier", "Rounds.id")
);


DROP TABLE IF EXISTS "CardsSongsSets" CASCADE;
CREATE TABLE "CardsSongsSets"
(
	"id" SERIAL NOT NULL PRIMARY KEY,
	"position" INT[2] NOT NULL DEFAULT ARRAY[5, 5]::INT[2],
	"Cards.id" INT NOT NULL,
	"SongsSets.id" INT NOT NULL,
	UNIQUE ("position", "Cards.id"),
	FOREIGN KEY ("Cards.id") REFERENCES "Cards" ("id"),
	FOREIGN KEY ("SongsSets.id") REFERENCES "SongsSets" ("id")
);
