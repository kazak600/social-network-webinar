from aiohttp import web


async def index(request):
    return web.Response(text='Hello Aiohttp!')


async def login(request):
    return web.Response(text='login Aiohttp!')


async def signup(request):
    return web.Response(text='signup Aiohttp!')
