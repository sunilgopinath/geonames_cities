import os
import pathlib
import subprocess

import pytest

from geonames_sunil.main import init

BASE_DIR = pathlib.Path(__file__).parent.parent
# Prepend src directory to python path
root = os.path.dirname(os.path.realpath(__file__))


@pytest.fixture
def app_db():
    subprocess.call([(BASE_DIR / 'sql' / 'install.sh').as_posix()], shell=True, cwd=BASE_DIR.as_posix())
