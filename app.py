import aiohttp_jinja2
import jinja2
import aiohttp
from aiohttp import web
import os
import zipfile

routes = web.RouteTableDef()

def html_response(document):
    s = open(document, "r")
    return web.Response(text=s.read(), content_type='text/html')

async def index_handler(request):
    return html_response('./templates/homepage.html')


async def json_passer(request):
    context = {'name': 'Andrew', 'surname': 'Svetlov'}
    input(context)
    response = aiohttp_jinja2.render_template('test.html',
                                              request,
                                              context)
    response.headers['Content-Language'] = 'eng'

    return response

async def read_zip(filename):
    with zipfile.ZipFile(os.path.join(os.getcwd()+'/static/Files/', filename), 'r') as zip_ref:
        zip_ref.extractall(os.path.join(os.getcwd()+'/static/Zip_Extracted/'))
    li = os.listdir(os.path.join(os.getcwd()+'/static/Zip_Extracted/'))

async def store_zip(request):

    reader = await request.multipart()
    zip = await reader.next()
    filename = zip.filename
    # You cannot rely on Content-Length if transfer is chunked.
    size = 0
    with open(os.path.join(os.getcwd()+'/static/Files/', filename), 'wb') as f:
        while True:
            chunk = await zip.read_chunk()  # 8192 bytes by default.
            if not chunk:
                break
            size += len(chunk)
            f.write(chunk)


    await read_zip(filename)
    input("checkpont 1")

    return web.HTTPFound('/jss')



app = web.Application()
app.add_routes(routes)
aiohttp_jinja2.setup(app,
    loader=jinja2.FileSystemLoader('./templates'))
app.router.add_get('/', index_handler)
app.router.add_post('/myfun', store_zip)
app.router.add_get('/jss', json_passer)
web.run_app(app)