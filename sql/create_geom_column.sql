SET ROLE 'geonames_user';

BEGIN;

SELECT AddGeometryColumn ('public','cities','geom',4326,'POINT',2);
UPDATE cities SET geom = ST_PointFromText('POINT(' || longitude || ' ' || latitude || ')', 4326);
COMMIT;