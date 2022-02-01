'''
Copyright Version: BETA
Developer: Pritul Dave
Organization: Maruti Tech Labs
This software is free to reuse
'''

from aiohttp import web
import jinja2
import aiohttp_jinja2
import os

#Setting up HTML page routing#
routes = web.RouteTableDef()
app = web.Application()
app.add_routes(routes)

#Setting up the jinja rendering#
def setup_jinja():
    aiohttp_jinja2.setup(app,loader=jinja2.FileSystemLoader('./templates'))

app['static_root_url'] = '/static'


setup_jinja()

ls = os.listdir(".")

if not 'static' in ls:
	os.mkdir("./static")
	os.mkdir("./static/Files")
	os.mkdir("./static/Zip_Extracted")
