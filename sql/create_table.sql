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