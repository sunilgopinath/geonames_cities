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


async def foo(files, conn):
    page_size = 2000
    page = []
    for file in files:
        with open(file, encoding='utf-8') as tsv:
            for row in csv.reader(tsv, delimiter='\t'):
                page.append(
                    (int(row[0]), row[1], float(row[4]), float(row[5]), row[8], row[10], row[11]) 
                )
                if len(page) >= page_size:
                    await insert(page, conn)
                    page = []

    await insert(page, conn)

async def copy_to(files, conn):
    for file in files:
        fff = os.getcwd()[:-5]
        print(fff)
        ff = file[3:]
        print(ff)
        stmt = "COPY cities from PROGRAM 'cut -f1,3,5,6,9,11,12 {}' null as '';".format(fff+ff)
        await conn.execute(stmt)

    
async def insert(rows, conn):
    result = await conn.copy_records_to_table('cities', records=rows)
    

async def main():
    conn = await asyncpg.connect(DB_URL)
    # files = await get_files(os.path.join(os.getcwd(), 'all'))
    files = await get_files('../all')
    await copy_to(files, conn)
    await conn.close()

t0 = time.time()
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
print(time.time() - t0), "seconds wall time"