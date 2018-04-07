import asyncio
import csv
import os
import time

import aiofiles
import asyncpg

import config


async def get_files(startdir):
    """Walks through the directory where the 'single line' files are kept and
       passes that value through to the process_files function

    """
    if os.path.exists(startdir) == False:
        logger.error('Cannot use connection')
        raise OSError(2, 'No such file or directory', startdir)

    return [os.path.join(dirpath, f) for dirpath, _, filenames in os.walk(startdir) for f in filenames]


async def foo(files, pool):
    page_size = 2000
    page = []
    for file in files:
        async with aiofiles.open(file, encoding='utf-8') as tsv:
            line = await tsv.readline()
            row = line.split('\t')
            try:
                page.append((int(row[0]), row[1], float(row[4]), float(row[5]), row[8], row[10], row[11]))
            except ValueError:
                # we are going to skip invalid data
                pass
            if len(page) >= page_size:
                await insert(page, pool)
                page = []

    await insert(page, pool)


async def insert(rows, pool):
    async with pool.acquire() as con:
        await con.copy_records_to_table('cities', records=rows)


async def main():
    pool = await asyncpg.create_pool(config.DSN)
    files = await get_files(config.DIRECTORY)
    await foo(files, pool)


t0 = time.time()
ioloop = asyncio.get_event_loop()
tasks = [ioloop.create_task(main())]
wait_tasks = asyncio.wait(tasks)
ioloop.run_until_complete(wait_tasks)
ioloop.close()
print(time.time() - t0), "seconds wall time"
