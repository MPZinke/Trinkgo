

DROP TABLE "Playlists" IF EXISTS;
CREATE TABLE "Playlists"
(
	"id" SERIAL NOT NULL PRIMARY KEY,
	"name" VARCHAR(100) NOT NULL,
	"url" TEXT NOT NULL,
	"is_deleted" BOOL NOT NULL
);



DROP TABLE "Songs" IF EXISTS;
CREATE TABLE "Songs"
(
	"id" SERIAL NOT NULL PRIMARY KEY,
	"name" VARCHAR(100),
	"url" TEXT NOT NULL,
	"start" INT NOT NULL DEFAULT 0,
	"duration" INT NOT NULL DEFAULT 0,
	"is_deleted" BOOL NOT NULL,
	"Playlists.id" INT NOT NULL,
	FOREIGN KEY ("Playlists.id") REFERENCES "Playlists"("id")
);



