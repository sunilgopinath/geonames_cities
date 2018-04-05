import asyncio
import asyncpg
import csv
import os
import time
from multiprocessing import Pool

DB_URL = 'postgresql://geonames_user@localhost/geonames_sunil'

async def get_files(startdir):
    """Walks through the directory where the 'single line' files are kept and
       passes that value through to the process_files function

    """
    if os.path.exists(startdir) == False:
        logger.error('Cannot use connection')
        raise OSError(2, 'No such file or directory', startdir)

    return  [os.path.join(dirpath, f) for dirpath, _, filenames in os.walk(startdir) for f in filenames]


async def foo(files, pool):
    """This is where I loop through the files, read 2000 lines into memory (will work on files of any size)
       send those to the insert function
    
    """
    page_size = 2000
    page = []
    for file in files:
        with open(file, encoding='utf-8') as tsv:
            for row in csv.reader(tsv, delimiter='\t'):
                page.append(
                    (int(row[0]), row[1], float(row[4]), float(row[5]), row[8], row[10], row[11]) 
                )
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
        await con.copy_records_to_table('cities', records=rows)
    

async def main():
    pool = await asyncpg.create_pool(DB_URL, min_size=10)
    # files = await get_files(os.path.join(os.getcwd(), 'all'))
    files = await get_files('../../all20')
    await foo(files, pool)
    await pool.close()

if __name__ == '__main__':
    t0 = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
    print(time.time() - t0), "seconds wall time"

