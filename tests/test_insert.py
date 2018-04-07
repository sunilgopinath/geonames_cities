"""
Integration tests. They need a running database.

Beware, they destroy your db using sudo.
"""
import os

import pytest

from conftest import BASE_DIR
from insert.loader import get_files


@pytest.mark.asyncio
async def test_get_files_bad_directory():
    with pytest.raises(OSError) as e_info:
        await get_files('./textx')


@pytest.mark.asyncio
async def test_get_files_success():
    test_dir = os.path.join(BASE_DIR, 'test_files')
    result = await get_files(test_dir)
    assert result == [os.path.join(test_dir, 'city2.txt'), os.path.join(test_dir, 'city1.txt')]
