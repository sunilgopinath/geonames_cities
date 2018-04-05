SET ROLE 'geonames_user';

BEGIN;

ALTER TABLE cities ADD PRIMARY KEY (geonameid);
CREATE INDEX IF NOT EXISTS idx_cities_geom ON public.cities USING gist(geom);
CREATE INDEX idx_cities_name ON cities(name);

COMMIT;