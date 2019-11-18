CREATE TABLE IF NOT EXISTS "taps" (
	"tap-id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"address"	TEXT NOT NULL UNIQUE,
	"longitude"	NUMERIC NOT NULL,
	"latitude"	NUMERIC NOT NULL,
	"picutre"	BLOB
);
