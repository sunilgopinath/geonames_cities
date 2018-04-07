import argparse
import asyncio
import logging
import sys

import aiozipkin as az
from trafaret_config import commandline

from aiohttp import web
from geonames_sunil.db import close_pg, init_pg
from geonames_sunil.routes import setup_routes
from geonames_sunil.utils import TRAFARET


async def init(argv):
    ap = argparse.ArgumentParser()
    commandline.standard_argparse_options(ap, default_config='./config/geonames.yaml')
    #
    # define your command-line arguments here
    #
    options = ap.parse_args(argv)

    config = commandline.config_from_options(options, TRAFARET)

    # setup application and extensions
    app = web.Application()

    endpoint = az.create_endpoint('aiohttp_server', ipv4='127.0.0.1', port=9001)

    zipkin_address = 'http://127.0.0.1:9411'
    tracer = await az.create(zipkin_address, endpoint, sample_rate=1.0)
    az.setup(app, tracer)

    # load config from yaml file in current dir
    app['config'] = config

    # create connection to the database
    app.on_startup.append(init_pg)
    # shutdown db connection on exit
    app.on_cleanup.append(close_pg)
    # setup views and routes
    setup_routes(app)

    return app


def main(argv):
    # init logging
    logging.basicConfig(level=logging.DEBUG)

    loop = asyncio.get_event_loop()

    app = loop.run_until_complete(init(argv))
    web.run_app(app, host=app['config']['host'], port=app['config']['port'])


if __name__ == '__main__':
    main(sys.argv[1:])
