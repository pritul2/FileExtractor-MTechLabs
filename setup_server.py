from aiohttp import web
import jinja2
import aiohttp_jinja2

#Setting up HTML page routing#
routes = web.RouteTableDef()
app = web.Application()
app.add_routes(routes)

#Setting up the jinja rendering#
def setup_jinja():
    aiohttp_jinja2.setup(app,loader=jinja2.FileSystemLoader('./templates'))
setup_jinja()



