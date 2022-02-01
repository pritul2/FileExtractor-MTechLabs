import setup_server
from setup_server import app
from aiohttp import web
import aiohttp_jinja2
import os
import zipfile

'''
HTML Parser to parse the html web pages
'''
class HtmlParser:
    def __init__(self):
        self.home_page_url = "./templates/homepage.html"
        pass

    # This function parse the html web page #
    def html_response(self,document):
        self.rd_ptr = open(document, "r")
        return web.Response(text=self.rd_ptr.read(), content_type='text/html')

    #Home page handler#
    async def index_handler(self,request):
        return self.html_response(self.home_page_url)


'''
Zip file related operations
'''
class ZipOps:
    def __init__(self):
        self.zip_storing_loc = "/static/Files/"
        self.zip_extracting_loc = "/static/Zip_Extracted/"
        self.zip_files_ls = None
        pass

    #Passing data of file names to html#
    @aiohttp_jinja2.template("file_selector.html")
    async def file_names_parser(self,request):
        self.zip_files_ls = os.listdir(os.getcwd()+self.zip_extracting_loc)
        self.context = {}

        cnt = 1
        for f in self.zip_files_ls:
            self.context['file'+str(cnt)] = f
            cnt+=1

        self.context['file_counts'] = cnt

        return {"Zip_Files":self.zip_files_ls}

    #Reading and Extracting the zip file contents#
    async def read_zip(self,filename):
        with zipfile.ZipFile(os.path.join(os.getcwd()+self.zip_storing_loc, filename), 'r') as zip_ref:
            zip_ref.extractall(os.path.join(os.getcwd()+self.zip_extracting_loc))

    #Webstreaming for reading the passed data of zip files#
    async def store_zip(self,request):
        reader = await request.multipart()
        zip = await reader.next()
        filename = zip.filename
        size = 0
        with open(os.path.join(os.getcwd()+self.zip_storing_loc, filename), 'wb') as f:
            while True:
                chunk = await zip.read_chunk()  # 8192 bytes by default.
                if not chunk:
                    break
                size += len(chunk)
                f.write(chunk)
        await self.read_zip(filename)
        return web.HTTPFound('/jss')

    @aiohttp_jinja2.template("downloader.html")
    async def pass_file(self,request):
        data = await request.post()
        self.files_to_pass = []
        print(data)
        for i in data.keys():
            print(i)
            self.files_to_pass.append("/Zip_Extracted/"+self.zip_files_ls[int(i)-1])
        return {"Selected_Files":self.files_to_pass}



html = HtmlParser()
zip_ops = ZipOps()

app.router.add_route('GET', '/', html.index_handler)
app.router.add_route('GET', '/jss', zip_ops.file_names_parser)
app.router.add_route('POST', '/myfun', zip_ops.store_zip)
app.router.add_route('POST', '/file_query', zip_ops.pass_file)

STATIC_PATH = os.path.join(os.path.dirname(__file__), "static")
app.router.add_static('/static/', STATIC_PATH, name='static')


#Run the web app#
web.run_app(app)