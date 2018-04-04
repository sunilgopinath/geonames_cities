SET ROLE 'geonames_user';

BEGIN;

CREATE EXTENSION IF NOT EXISTS postgis;

--
-- Create model Choice
--
CREATE TABLE IF NOT EXISTS cities ("id" INT,
                "name" VARCHAR(200),
                "geom" GEOMETRY(Point, 4326),
                "latitude" float,
                "longitude" float,
                "country_code" varchar(2),
                "admin1" varchar(20),
                "admin2" varchar(80)
            );
COMMIT;