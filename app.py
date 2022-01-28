from aiohttp import web
import os
import zipfile

routes = web.RouteTableDef()

def html_response(document):
    s = open(document, "r")
    return web.Response(text=s.read(), content_type='text/html')

async def index_handler(request):
    return html_response('./templates/homepage.html')

async def read_zip(filename):
    with zipfile.ZipFile(os.path.join(os.getcwd()+'/static/Files/', filename), 'r') as zip_ref:
        zip_ref.extractall(os.path.join(os.getcwd()+'/static/Zip_Extracted/'))
    li = os.listdir(os.path.join(os.getcwd()+'/static/Zip_Extracted/'))
    print(li)
    return

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
    return web.Response(text='{} sized of {} successfully stored'
                             ''.format(filename, size))

app = web.Application()
app.add_routes(routes)
app.router.add_get('/', index_handler)
app.router.add_post('/myfun', store_zip)
web.run_app(app)