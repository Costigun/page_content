from aiohttp import web
from routes import setup_routes
import jinja2
import aiohttp_jinja2
from query import BASE_DIR

#TODO: count page views per session, download file from media ?

app = web.Application()
aiohttp_jinja2.setup(app,loader=jinja2.FileSystemLoader(str(BASE_DIR / 'templates')))
setup_routes(app)

web.run_app(app)



