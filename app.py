from aiohttp import web

routes = web.RouteTableDef()

def html_response(document):
    s = open(document, "r")
    return web.Response(text=s.read(), content_type='text/html')

async def index_handler(request):
    return html_response('./templates/homepage.html')

async def do_myfun(request):
    input()

app = web.Application()
app.add_routes(routes)
app.router.add_get('/', index_handler)
app.router.add_post('/myfun', do_myfun)
web.run_app(app)