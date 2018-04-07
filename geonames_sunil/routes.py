import pathlib

from .handlers import city, healthCheck, neighbors

PROJECT_ROOT = pathlib.Path(__file__).parent


def setup_routes(app):
    app.router.add_get('/city/{city_name}', city)
    app.router.add_get('/neighbors', neighbors)
    app.router.add_get('/healthz', healthCheck)
