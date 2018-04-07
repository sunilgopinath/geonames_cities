import asyncio
import csv
import logging
import os
import time

import asyncpg

import config

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)


async def get_files(startdir):
    """Walks through the directory where the 'single line' files are kept and
       passes that value through to the process_files function

    """
    if os.path.exists(startdir) == False:
        logger.error("OS error: {0}".format(startdir))
        raise OSError(2, 'No such file or directory', startdir)

    return [os.path.join(dirpath, f) for dirpath, _, filenames in os.walk(startdir) for f in filenames]


async def process_files(files, pool):
    """This is where I loop through the files, read 2000 lines into memory (will work on files of any size)
       send those to the insert function
    
    """
    page_size = config.PAGE_SIZE
    page = []
    for file in files:
        with open(file, encoding='utf-8') as tsv:
            for row in csv.reader(tsv, delimiter='\t'):
                page.append((int(row[0]), row[1], float(row[4]), float(row[5]), row[8], row[10], row[11]))
                if len(page) >= page_size:
                    await insert(pool, page)
                    page = []

    await insert(pool, page)


async def insert(pool, page):
    """Use the connection pool to insert the records. I use the copy command instead of INSERT as
       it is much much faster and we don't have to worry about data loss as wel have the original
       dataset readily available.

    """
    async with pool.acquire() as con:
        await con.copy_records_to_table('cities', records=page)


async def main():
    # setup db connection
    pool = await asyncpg.create_pool(
        host=config.DATABASE_CONFIG['host'],
        port=config.DATABASE_CONFIG['port'],
        user=config.DATABASE_CONFIG['user'],
        database=config.DATABASE_CONFIG['dbname'],
        password=config.DATABASE_CONFIG['password'],
    )
    # walk through the directory containing the single line file
    files = await get_files(config.DIRECTORY)

    # this pages the data and saves it to the db
    await process_files(files, pool)

    # finally close the pool
    await pool.close()


if __name__ == '__main__':
    t0 = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
    print(time.time() - t0), "seconds wall time"
