import asyncpg
import shapely.geometry
import shapely.wkb
from shapely.geometry.base import BaseGeometry


class RecordNotFound(Exception):
    """Requested record in database was not found"""


async def init_pg(app):
    """Creates a client connetion based off the values supplied in the geonames.yml

    """
    conf = app['config']['postgres']
    conn = await asyncpg.connect(
        user=conf['user'], password=conf['password'], database=conf['database'], host=conf['host']
    )
    app['db'] = conn


async def close_pg(app):
    """Closes the connection after all the operations

    """
    await app['db'].close()


async def get_city(conn, city_name):
    """Selects the city based on the name. It is an exact match

    """
    results = await conn.fetch('SELECT * from cities where name = $1', city_name.title())
    if not results:
        msg = "City information for: {} does not exist"
        raise RecordNotFound(msg.format(city_name))
    return results


async def get_neighbors(conn, longitude, latitude, number):
    """"Gets the number nearest neighbors based off the postgis KNN algorithm

    """
    results = await conn.fetch(
        'SELECT * from cities order by geom <-> ST_SetSRID(ST_MakePoint($1, $2), 4326) limit $3', longitude, latitude,
        number
    )
    if not results:
        msg = "Neighbors for long: {} lat: {} do not exist"
        raise RecordNotFound(msg.format(longitude), latitude)
    return results
