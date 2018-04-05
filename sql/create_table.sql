SET ROLE 'geonames_user';

BEGIN;

CREATE EXTENSION IF NOT EXISTS postgis;

--
-- Create model Choice
--
CREATE TABLE IF NOT EXISTS cities ("geonameid" INT,
                "name" VARCHAR(200),
                "latitude" float,
                "longitude" float,
                "country_code" varchar(2),
                "admin1" varchar(20),
                "admin2" varchar(80)
            );

COMMIT;

create table geoname (
	geonameid	int,
	name varchar(200),
	asciiname varchar(200),
	alternatenames text,
	latitude float,
	longitude float,
	fclass char(1),
	fcode varchar(10),
	country varchar(2),
	cc2 varchar(60),
	admin1 varchar(20),
	admin2 varchar(80),
	admin3 varchar(20),
	admin4 varchar(20),
	population bigint,
	elevation int,
	gtopo30 int,
	timezone varchar(40),
	moddate date
 );
 
COMMIT;