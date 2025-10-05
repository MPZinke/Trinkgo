

DROP TABLE IF EXISTS "Playlists" CASCADE;
CREATE TABLE "Playlists"
(
	"id" SERIAL NOT NULL PRIMARY KEY,
	"uri" CHAR(22) NOT NULL,
	"name" TEXT NOT NULL,
	"is_deleted" BOOL NOT NULL DEFAULT FALSE
);


DROP TABLE IF EXISTS "Songs" CASCADE;
CREATE TABLE "Songs"
(
	"id" SERIAL NOT NULL PRIMARY KEY,
	"uri" CHAR(22) NOT NULL,
	"name" TEXT NOT NULL,
	"album" TEXT NOT NULL,
	"artists" TEXT NOT NULL,
	"artwork" TEXT DEFAULT NULL,
	"length" INT NOT NULL DEFAULT 0,
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
	"start" INT NOT NULL DEFAULT 0,
	"duration" INT NOT NULL DEFAULT 0,
	"is_deleted" BOOL NOT NULL DEFAULT FALSE,
	"Songs.id" INT NOT NULL,
	"PlaylistsSets.id" INT NOT NULL,
	FOREIGN KEY ("Songs.id") REFERENCES "Songs" ("id"),
	FOREIGN KEY ("PlaylistsSets.id") REFERENCES "PlaylistsSets" ("id")
);


DROP TABLE IF EXISTS "Cards" CASCADE;
CREATE TABLE "Cards"
(
	"id" SERIAL NOT NULL PRIMARY KEY,
	"Playlists.id" INT NOT NULL,
	"is_deleted" BOOL NOT NULL DEFAULT FALSE,
	"size" INT[2] NOT NULL DEFAULT ARRAY[5, 5]::INT[2],
	FOREIGN KEY ("Playlists.id") REFERENCES "Playlists" ("id")
);


DROP TABLE IF EXISTS "CardsSongs" CASCADE;
CREATE TABLE "CardsSongs"
(
	"id" SERIAL NOT NULL PRIMARY KEY,
	"order" INT NOT NULL,
	"Songs.id" INT NOT NULL,
	"Playlists.id" INT NOT NULL,
	"Cards.id" INT NOT NULL,
	UNIQUE ("order", "Cards.id"),
	FOREIGN KEY ("Songs.id") REFERENCES "Songs" ("id"),
	FOREIGN KEY ("Playlists.id") REFERENCES "Playlists" ("id"),
	FOREIGN KEY ("Cards.id") REFERENCES "Cards" ("id")
);


DROP TABLE IF EXISTS "Games" CASCADE;
CREATE TABLE "Games"
(
	"id" SERIAL NOT NULL PRIMARY KEY,
	"started_date" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	"end_date" TIMESTAMP DEFAULT NULL,
	"Playlists.id" INT NOT NULL,
	FOREIGN KEY ("Playlists.id") REFERENCES "Playlists" ("id")
);


DROP TABLE IF EXISTS "Rounds" CASCADE;
CREATE TABLE "Rounds"
(
	"id" SERIAL NOT NULL PRIMARY KEY,
	"order" INT NOT NULL,
	"Games.id" INT NOT NULL,
	"Playlists.id" INT NOT NULL,
	"Songs.id" INT NOT NULL,
	"Cards.id" INT DEFAULT NULL,  -- board that won this round
	FOREIGN KEY ("Games.id") REFERENCES "Games" ("id"),
	FOREIGN KEY ("Playlists.id") REFERENCES "Playlists" ("id"),
	FOREIGN KEY ("Songs.id") REFERENCES "Songs" ("id"),
	FOREIGN KEY ("Cards.id") REFERENCES "Cards" ("id")
);
