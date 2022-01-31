from aiohttp import web

routes = web.RouteTableDef()

def html_response(document):
    s = open(document, "r")
    return web.Response(text=s.read(), content_type='text/html',data=data)

async def index_handler(request):
    data = {'some': 'data'}
    web.json_response(data)


app = web.Application()
app.add_routes(routes)
app.router.add_get('/', index_handler)
web.run_app(app)