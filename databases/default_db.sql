DROP TABLE IF EXISTS "reviews";
DROP TABLE IF EXISTS "taps";
DROP TABLE IF EXISTS "users";

CREATE TABLE IF NOT EXISTS "users"(
	"id"  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"userName" TEXT NOT NULL UNIQUE,
	"password" TEXT NOT NULL,
	"role" BOOLEAN NOT NULL
	-- 0 will be regular user and 1 will be admin
);

CREATE TABLE IF NOT EXISTS "taps" (
	"id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"address" TEXT NOT NULL,
	"latitude"	TEXT NOT NULL,
	"longitude" TEXT NOT NULL,
	"picture"	TEXT,
	"userID" INTEGER NOT NULL,
	"postDate" DATE,
	"description" TEXT,
	FOREIGN KEY("userID") REFERENCES users("id")
);

CREATE TABLE IF NOT EXISTS "reviews"(
	"id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"comment" TEXT NOT NULL,
	"date" TEXT NOT NULL,
	"tapID" INTEGER NOT NULL,
	"userID" INTEGER NOT NULL,
	FOREIGN KEY("tapID") REFERENCES taps("id"),
	FOREIGN KEY("userID") REFERENCES users("id")
	/* connects the tap-id in the taps table to the comments
	table for when we start to store comments about the taps*/
);

INSERT INTO 'users'('id','username','password','role') VALUES ("1","Anonymus","password","0");
