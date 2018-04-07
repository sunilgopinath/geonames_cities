# Geonames Data

Primer Distributed Computing Challenge. Here I detail how to run the challenge and my thought processes.

# Pre-requisites

- [Python3.6](https://www.python.org/downloads/release/python-365/)
- [Postgres](https://www.postgresql.org/)
- [PostGIS extension](https://postgis.net/)

# Running the insert script

1. Save zip file into a directory, let's call it base_dir
2. Find `sql/install.sh`
3. Inspect the db values (I deliberately personalized the name so as to not conflict)
```sh
base_dir$> cd geonames_sunil
base_dir/geonames_sunil$> python3 -m virtualenv env
base_dir/geonames_sunil$> source env/bin/activate
(env) base_dir/geonames_sunil$> pip install -e .
(env) base_dir/geonames_sunil$> bash sql/install.sh
....
```
4. find `insert/config.py`
5. Edit the values (if need be), please make consistent with `.sh` file
6. Execute:
```sh
python insert/loader.py
```
7. Wait for it to finish

### Addressing Instructions
> Processing

For the columns, I chose 
columns: 1, 2, 5, 6, 9, 11, 12

I chose column2 based on the latin-1 encoding which postgres handles

> Not only should this data be persisted...

In order to address this i I wrote a very basic web app to access the data using `aysnchttp`. If you have followed the above instructions you should be able to run it by
```sh
python -m geonames_sunil
```
Then navigating to 
http://localhost:8080/neighbors?longitude=-73.98569&latitude=40.74844&number=10

and 

http://localhost:8080/city/<city_name> (ex http://localhost:8080/city/sydney)

In keeping with the time restrictions and wanting to focus on the optimization of speed of insertion this webapp is *very* basic.

> As is (Single file)...

I have a page size setting (configurable, see `insert/config.py` currently set to 2000 in order to keep the memory usage down but I tested with loading the whole thing into memory and it worked fine.
```sh
(env) ➜  geonames_sunil git:(master) ✗ python insert/loader.py
70.43773221969604
(env) ➜  polls git:(master) ✗ bash sql/post_process.sh
SET ROLE 'geonames_user';
...
```
> As multiple files (e.g. Each line as an individual file, same format) 

In order to do this, you have to edit the `insert/config.py` and enter the directory where the files are kept and re-run the previous command.

NB. I personally could not create a directory with 12m single line files, the most I could get to is 600k

> The design should optimize for scalability...

The honest truth here is that as much as I tried to optimize for scalability I could not seem to speed up the file processing when there are so many small files.

### Final Solution
I use the async library in built in python3. I also use the asyncpg library to access postgres in order to speed it up as much as possible.
#### Explanation:
1. Get all the files from the directory (~12m)
2. Pass that list to the `process_files()` which iterates over the files reading in the *PAGE_SIZE* amount of files before sending that off for db insertion

 - As the amount of files increase the computer resources do not necessarily increase because I am only reading the *PAGE_SIZE* into memory and using the async libraries
 - Developer ease of use - I believe that starting the python script is very easy. I did not make a multi-tier application in order to best show in one class how the program flows.
 - Tech dependencies are python3 async libraries and out of the box postgres

### Limitations
- The system unfortunately does get into a linear increase situation with the amount of files read/written to the database. The bottleneck I see is the reading/writing of 100s of 1000s of small files. When there is one single file is is very fast but the IO in reading/writing small files is a hurdle I was not able to figure out.

I have included the numerous experiments to try and speed it up but got basically the same time (except for the use of `INSERT` which took one ~40mins to execute.

- Reprocessing data: With `COPY` it is very easy to reprocess data.
- Non-trivial increases...: Adding new fields will not be a problem. If a city's geo information changes then it will cause an update to the index and `geom` field. Adding an index to the geom field does take a long time to index but updating can be performed without a long delay.
- Monitoring/Alerting: In terms of monitoring the script. Upon completion of the insertion, a script to test the length of the 

[See Appendix for full output](#appendix)


# Single File Solution (POC)

## Prerequisite
- single 12m record file
- editor

1. Find the file `sql/single_file.sql`
2. Replace <PLACEHOLDER_TEXT> with full path to file eg:
```
COPY cities from PROGRAM 'cut -f1,3,5,6,9,11,12 <PLACEHOLDER_TEXT>'  null  as  '';

TO 
...
COPY cities from PROGRAM 'cut -f1,3,5,6,9,11,12 /Users/sunilgopinath/geonames/allCountries.txt'  null  as  '';
...
```
3. Inspect the `sql/single_file.sh` and make sure the credentials are acceptable.
4. Ensure you are in the root directory
```sh
$> bash sql/single_file.sh
```

### Explanation

Postgres' `COPY`  command is purpose built for the task of mass insertion from a large file.

Cons: Only basic pre-processing of tsv can be performed so the performance gained by the almost instant insertion of raw data
ex: 
```sh
COPY cities from PROGRAM 'cut -f1,3,5,6,9,11,12 /Users/sunilgopinath/Interview/trial/allCountries.txt' null as '';
COPY 11704735
Time: 47260.379 ms (00:47.260)
```
is slightly offset by creating the `geometry` column, primary key and indices (in our case the geometry and name fields)


[See Appendix for manual output](#appendix)

# Appendix

### Expected output of running single file
```sh

```

### Expected output of running `sql/single_file.sh`
```sh
(env) ➜  polls git:(master) ✗ bash sql/single_file.sh
Starting to load records into a fresh database...
NOTICE:  database "geonames_sunil" does not exist, skipping
DROP DATABASE
DROP ROLE
CREATE ROLE
ALTER ROLE
CREATE DATABASE
GRANT
SET ROLE 'geonames_user';
SET
BEGIN;
BEGIN
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION
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
CREATE TABLE
COMMIT;
COMMIT
SET ROLE 'geonames_user';
SET
BEGIN;
BEGIN
COPY cities from PROGRAM 'cut -f1,3,5,6,9,11,12 /Users/sunilgopinath/Interview/trial/allCountries.txt' null as '';
COPY 11704735
COMMIT;
COMMIT
SET ROLE 'geonames_user';
SET
BEGIN;
BEGIN
SELECT AddGeometryColumn ('public','cities','geom',4326,'POINT',2);
                addgeometrycolumn
-------------------------------------------------
 public.cities.geom SRID:4326 TYPE:POINT DIMS:2
(1 row)

UPDATE cities SET geom = ST_PointFromText('POINT(' || longitude || ' ' || latitude || ')', 4326);
UPDATE 11704735
COMMIT;
COMMIT
SET ROLE 'geonames_user';
SET
BEGIN;
BEGIN
ALTER TABLE cities ADD PRIMARY KEY (geonameid);
ALTER TABLE
CREATE INDEX IF NOT EXISTS idx_cities_geom ON public.cities USING gist(geom);
CREATE INDEX
CREATE INDEX idx_cities_name ON cities(name);
CREATE INDEX
COMMIT;
COMMIT
Records loaded in 10 minutes and 53 seconds.
```