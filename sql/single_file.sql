SET ROLE 'geonames_user';

BEGIN;

COPY cities from PROGRAM 'cut -f1,2,5,6,9,11,12 /Users/sunilgopinath/Interview/trial/allCountries.txt' null as '';

COMMIT;