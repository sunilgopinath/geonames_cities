import pathlib
import subprocess

import pytest

BASE_DIR = pathlib.Path(__file__).parent.parent


@pytest.fixture
def app_db():
    subprocess.check_output(
        [(BASE_DIR / 'sql' / 'test' / 'install.sh').as_posix()], shell=True, cwd=BASE_DIR.as_posix()
    )
