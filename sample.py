import asyncio
import asyncpg
import csv
import os

DB_URL = 'postgresql://postgres@localhost/test'

async def get_files(startdir):
    """Walks through the directory where the 'single line' files are kept and
       passes that value through to the process_files function

    """
    if os.path.exists(startdir) == False:
        logger.error('Cannot use connection')
        raise OSError(2, 'No such file or directory', startdir)

    return  [os.path.join(dirpath, f) for dirpath, _, filenames in os.walk(startdir) for f in filenames]


async def foo(files):
    page_size = 2000
    page = []
    for file in files:
        with open(file, encoding='utf-8') as tsv:
            for row in csv.reader(tsv, delimiter='\t'):
                page.append(
                    (int(row[0]), row[1], float(row[4]), float(row[5]), row[8], row[10], row[11]) 
                )
                if len(page) >= page_size:
                    await insert(page)
                    page = []

    await insert(page)

    
async def insert(rows):
    conn = await asyncpg.connect(DB_URL)
    result = await conn.copy_records_to_table('cities', records=rows)
    print(result)
    await conn.close()
    

async def main():
    files = await get_files(os.path.join(os.getcwd(), 'all'))
    await foo(files)


ioloop = asyncio.get_event_loop()
tasks = [ioloop.create_task(main())]
wait_tasks = asyncio.wait(tasks)
ioloop.run_until_complete(wait_tasks)
ioloop.close()
