import os
import re

from setuptools import find_packages, setup


def read_version():
    regexp = re.compile(r"^__version__\W*=\W*'([\d.abrc]+)'")
    init_py = os.path.join(os.path.dirname(__file__), 'geonames_sunil', '__init__.py')
    with open(init_py) as f:
        for line in f:
            match = regexp.match(line)
            if match is not None:
                return match.group(1)
        else:
            msg = 'Cannot find version in geonames_sunil/__init__.py'
            raise RuntimeError(msg)


install_requires = ['aiohttp', 'asyncpg', 'trafaret-config']

setup(
    name='geonames_sunil',
    version=read_version(),
    description='Primer AI Distributed Computing Challenge',
    platforms=['POSIX'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    zip_safe=False
)
