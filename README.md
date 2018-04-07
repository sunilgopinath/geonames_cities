# Playing around with Geonames

Looking at the geonames dataset

# Pre-requisites

- [Python3.6](https://www.python.org/downloads/release/python-365/)
- [Postgres](https://www.postgresql.org/)
- [PostGIS extension](https://postgis.net/)

# Running the insert script

### Quick start

```sh
$> git clone git@github.com:sunilgopinath/geonames_cities.git
geoname_cities$> cd geoname_cities
geoname_cities$> vim insert/config-prod.ini (add the location of the directory)
geoname_cities$> make create_venv
geoname_cities$> source env/bin/activate
geoname_cities$> make install
geoname_cities$> make load & echo $! > pid.txt
[1] 84944
./load.sh
Starting to load records...
...

COMMIT
74.12071490287781
SET ROLE 'geonames_user';
SET
...
COMMIT
Finished loading records.
Records loaded in 11 minutes and 20 seconds.
```

### To run tests
```sh
geoname_cities$> make install-deps
geoname_cities$> make test
make test
...
=============================================================================== test session starts ===
....

3 passed in 2.34 seconds

```

### To test nearest neighbour/city queries (API)
```sh
geoname_cities$>python -m geonames_sunil
geonames_cities$> docker run -d -e \
  COLLECTOR_ZIPKIN_HTTP_PORT=9411 \
  -p 5775:5775/udp \
  -p 6831:6831/udp \
  -p 6832:6832/udp \
  -p 5778:5778 \
  -p 16686:16686 \
  -p 14268:14268 \
  -p 9411:9411 \
  jaegertracing/all-in-one:latest

geoname_cities$> curl -H "Content-Type: application/json" 'http://localhost:8080/city/sydney' | jq
[
  {
    "geonameid": 6160752,
    "name": "Sydney",
    "latitude": 46.15014,
    "longitude": -60.18175,
    "country_code": "CA",
    "admin1": "07",
    "admin2": "",
    "geom": "0101000020E61000002506819543174EC025E99AC937134740"
  }
  ...
  geoname_cities$> curl -H "Content-Type: application/json" 'http://localhost:8080/neighbors?longitude=-73.98569&latitude=40.74844&number=10' | jq
  [
  {
    "geonameid": 5142464,
    "name": "WBAI-FM (New York)",
    "latitude": 40.74844,
    "longitude": -73.98569,
    "country_code": "US",
    "admin1": "NY",
    "admin2": "061",
    "geom": "0101000020E6100000A27F828B157F52C05682C5E1CC5F4440"
  },
  {
    "geonameid": 5142481,
    "name": "WBLS-FM (New York)",
    "latitude": 40.74844,
    "longitude": -73.98569,
    "country_code": "US",
    "admin1": "NY",
    "admin2": "061",
    "geom": "0101000020E6100000A27F828B157F52C05682C5E1CC5F4440"
  },
  ...
```
Visit http://localhost:16686/search and search on `geonames_app` and find your GETs ('postgres:select:get_neighbors', 'postgres:select:get_city'). This is to illustrate that POSTGIS can answer these questions very quickly.

### Single file load

- single 12m record file

1. Find the file `sql/single_file.sql`
2. Replace <PLACEHOLDER_TEXT> with full path to file eg:
```
COPY cities from PROGRAM 'cut -f1,3,5,6,9,11,12 <PLACEHOLDER_TEXT>'  null  as  '';

TO 
...
COPY cities from PROGRAM 'cut -f1,3,5,6,9,11,12 ~/allCountries.txt'  null  as  '';
...
```
3. Inspect the `sql/single_file.sh` and make sure the credentials are acceptable.
4. Ensure you are in the root directory
```sh
$> make load-as-single-file
```

### Troubleshooting
1. `.sh` files do not load. Set permission ex: `chmod a+rx <file_name>.sh`
```sh
make load-as-single-file
./sql/single_file.sh
make: ./sql/single_file.sh: Permission denied
make: *** [load-as-single-file] Error 1
chmod a+rx sql/single_file.sh
```
2. Script seems to have finished loading but program still running. Hopefully it is just the index creation taking a very long time
