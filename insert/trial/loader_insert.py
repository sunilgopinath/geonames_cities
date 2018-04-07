import asyncio
import csv
import logging
import os
import time

import asyncpg

import config

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)


async def run(conn):
    """General starter function after we know the connection can be established

    """
    stmt = await conn.prepare(
        '''
        INSERT INTO cities(name, geom, latitude, longitude, country_code, admin1, admin2, id) 
        VALUES($1, ST_SetSRID(ST_MakePoint($3, $2), 4326), $3, $2, $4, $5, $6, $7);
        '''
    )
    files = await get_files(config.DIRECTORY)
    [ await process_files(f, stmt) for f in files]
    await cleanup(conn)


async def get_files(startdir):
    """Walks through the directory where the 'single line' files are kept and
       passes that value through to the process_files function

    """
    return [os.path.join(dirpath, f) for dirpath, _, filenames in os.walk(startdir) for f in filenames]


async def process_files(path, stmt):
    """Reading and persisting the file. I use a geometry field for the nearest neighbour query

    """
    with open(path, encoding="utf-8") as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        for row in reader:
            try:
                await stmt.fetchval(row[1], float(row[4]), float(row[5]), row[8], row[10], row[11], int(row[0]))
            except Exception as e:
                logger.error("Could not insert record: {0}".format(row))
                raise


async def init_app():
    """Initialize a connection to the database, use postgis and create the table.
    
    NB: the indexes will come later
    """
    try:
        conn = await asyncpg.connect(config.DSN)
        # Installs the postgis addon
        await conn.execute('''
            CREATE EXTENSION IF NOT EXISTS postgis;
        ''')
        # Execute a statement to create a new table.
        await conn.execute(
            '''
            CREATE TABLE IF NOT EXISTS cities (
                id INT,
                name VARCHAR(200),
                geom GEOMETRY(Point, 4326),
                latitude float,
                longitude float,
                country_code varchar(2),
                admin1 varchar(20),
                admin2 varchar(80)
            )
        '''
        )
    except:
        logger.error('Error trying to set up the database')

    return conn


async def cleanup(conn):
    """Adding back the indices after the bulk import

    """
    # It's faster to add back indexes after bulk loading - ASSUMPTION: ids are unique from dataset
    await conn.execute('''
        ALTER TABLE cities ADD PRIMARY KEY (id);
    ''')
    # Index for geometry, specifically nearest neighbor query
    await conn.execute(
        '''
        CREATE INDEX IF NOT EXISTS idx_cities_geom ON public.cities USING gist(geom);
    '''
    )
    await conn.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        t0 = time.time()
        logger.info('-- Loop started --')
        task = asyncio.ensure_future(init_app())
        conn = loop.run_until_complete(task)
        loop.run_until_complete(run(conn))
    except Exception as err:
        print("Terminating application: {0}".format(err))
    finally:
        loop.close()
        logger.info('-- Loop closed --')
        print(time.time() - t0), "seconds wall time"
