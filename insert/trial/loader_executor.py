import asyncio
import concurrent.futures
import csv
import io
import os
import time

import config
import psycopg2
from psycopg2.pool import ThreadedConnectionPool


tcp = ThreadedConnectionPool(1, 10, config.DSN)


def get_files(startdir):
    """Walks through the directory where the 'single line' files are kept and
       passes that value through to the process_files function

    """
    return [os.path.join(dirpath, f) for dirpath, _, filenames in os.walk(startdir) for f in filenames]


def process_files(files):
    for file in files:
        save_file(file)


def save_file(file):
    conn = tcp.getconn()
    cur = conn.cursor()
    with open(file, encoding='utf-8') as tsv:
        cur.copy_from(tsv, 'geoname', null='')
        conn.commit()
    tcp.putconn(conn)


async def main(loop):
    # Create a pool of processes. By default, one is created for each CPU in your machine.
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # Get a list of files to process
        files = get_files(config.DIRECTORY)

        # Process the list of files, but split the work across the process pool to use all CPUs!
        await loop.run_in_executor(executor, process_files, files)
    # executor.submit(process_files, files)


t0 = time.time()
loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
loop.close()
print(time.time() - t0), "seconds wall time"
