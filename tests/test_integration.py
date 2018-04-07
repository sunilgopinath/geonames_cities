import configparser
import os

import asyncpg
import pytest

from conftest import BASE_DIR
from insert.loader import read_files


@pytest.mark.asyncio
async def test_load(app_db):
    config = configparser.ConfigParser()
    config.read("{0}/insert/config-test.ini".format(BASE_DIR))
    pool = await asyncpg.create_pool(
        host=config['DATABASE_CONFIG']['HOST'],
        port=config['DATABASE_CONFIG']['PORT'],
        user=config['DATABASE_CONFIG']['USER'],
        database=config['DATABASE_CONFIG']['DBNAME'],
        password=config['DATABASE_CONFIG']['PASSWORD'],
    )
    async with pool.acquire() as con:
        values = await con.fetch('''SELECT * FROM cities''')

    assert values == []

    # setup files
    files = [os.path.join(BASE_DIR, 'test_files', 'city2.txt'), os.path.join(BASE_DIR, 'test_files', 'city1.txt')]

    print("!@#!@#", read_files)
    await read_files(files, int(config['APP']['PAGE_SIZE']), pool)

    async with pool.acquire() as con:
        values_after_insert = await con.fetch('''SELECT * FROM cities''')

    assert len(values_after_insert) == 2
