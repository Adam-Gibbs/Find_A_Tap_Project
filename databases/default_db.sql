CREATE TABLE IF NOT EXISTS "taps" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"address" TEXT NOT NULL,
	"coordinates"	TEXT NOT NULL UNIQUE,
	"picture"	BLOB
);

CREATE TABLE IF NOT EXISTS "reviews"(
	"id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"tap-id" INTEGER NOT NULL,
	"comment" TEXT NOT NULL,
	"star-review" INTEGER NOT NULL,
	"date" TEXT NOT NULL,
	FOREIGN KEY("tap-id") REFERENCES taps("id")
	/* connects the tap-id in the taps table to the comments
	table for when we start to store comments about the taps*/
);
