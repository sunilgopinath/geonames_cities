"""
Integration tests. They need a running database.

Beware, they destroy your db using sudo.
"""
import asyncio
import os

import pytest

from conftest import BASE_DIR
from insert.loader import get_files, process_files


def _run(coro):
    """Run the given coroutine."""
    return asyncio.get_event_loop().run_until_complete(coro)


def test_get_files_bad_directory():
    with pytest.raises(OSError) as e_info:
        _run(get_files('./textx'))


def test_get_files_success():
    test_dir = os.path.join(BASE_DIR, 'test_files')
    result = _run(get_files(test_dir))
    assert result == [os.path.join(test_dir, 'city2.txt'), os.path.join(test_dir, 'city1.txt')]
