# Playing around with Geonames

Primer Distributed Computing Challenge. Here I detail how to run the challenge and my thought processes.

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
geoname_cities$> python3 -m virtualenv env
geoname_cities$> source env/bin/activate
geoname_cities$> pip install -e .
geoname_cities$> make load
make load
./load.sh & echo  > pid.txt
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
geoname_cities$> pip install -r requirements.txt
geoname_cities$> make test

```

### To test nearest neighbour/city queries (API)
```sh
geoname_cities$>python -m geonames_sunil
geoname_cities$> curl
```
