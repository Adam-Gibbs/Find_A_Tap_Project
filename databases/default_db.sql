CREATE TABLE IF NOT EXISTS "taps" (
	"tap-id" INTEGER NOT NULL UNIQUE AUTOINCREMENT,
	"longitude"	NUMERIC NOT NULL,
	"latitude"	NUMERIC NOT NULL,
	"picture"	BLOB,
	PRIMARY KEY(longitude, latitude)
);

CREATE TABLE IF NOT EXISTS "reviews"(
	"comment-id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"tap-id" INTEGER NOT NULL,
	"comment" TEXT NOT NULL,
	"star-review" INTEGER NOT NULL,
	"date" TEXT NOT NULL,
	FOREIGN KEY("tap-id") REFERENCES taps("tap-id")
	/* connects the tap-id in the taps table to the comments
	table for when we start to store comments about the taps*/
);
