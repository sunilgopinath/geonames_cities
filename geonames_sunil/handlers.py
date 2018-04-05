import json

from aiohttp import web

from . import db


async def city(request):
    city_name = request.match_info['city_name']
    try:
        results = await db.get_city(request.app['db'], city_name.title())
    except db.RecordNotFound as e:
        raise web.HTTPNotFound(text=str(e))

    return web.json_response(json.dumps([dict(ob) for ob in results]))


async def neighbors(request):
    """Return the k nearest neighbors.

    >>> curl 'http://localhost:8080/neighbors?longitude=-73.98569&latitude=40.74844&number=10'
    "[{\"id\": 5142464, \"name\": \"WBAI-FM (New York)\", \"geom\": \"0101000020E6100000A27F828B157F52C05682C5E1CC5F4440\", \"latitude\": -73.98569, \"longitude\": 40.74844, \"country_code\": \"US\", \"admin1\": \"NY\", \"admin2\": \"061\"}, 
    {\"id\": 5142503, \"name\": \"WCBS-FM (New York)\", \"geom\": \"0101000020E6100000A27F828B157F52C05682C5E1CC5F4440\", \"latitude\": -73.98569, \"longitude\": 40.74844, \"country_code\": \"US\", \"admin1\": \"NY\", \"admin2\": \"061\"}, 
    {\"id\": 5142481, \"name\": \"WBLS-FM (New York)\", \"geom\": \"0101000020E6100000A27F828B157F52C05682C5E1CC5F4440\", \"latitude\": -73.98569, \"longitude\": 40.74844, \"country_code\": \"US\", \"admin1\": \"NY\", \"admin2\": \"061\"},
    ...]
    """

    longitude = float(request.query["longitude"])
    latitude = float(request.query["latitude"])
    number = int(request.query["number"])
    results = await db.get_neighbors(request.app['db'], longitude, latitude, number)

    return web.json_response(json.dumps([dict(ob) for ob in results]))

async def healthCheck(request):
    """Return 200 to say the application is healthy.

    
    """
    return web.HTTPOk()
