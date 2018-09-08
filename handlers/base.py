import aiohttp_jinja2

from datetime import datetime

from aiohttp import web
from aiohttp_session import get_session


class Index(web.View):

    @aiohttp_jinja2.template('index.html')
    async def get(self):
        conf = self.app['config']
        return dict(conf=conf)


class Login(web.View):

    @aiohttp_jinja2.template('login.html')
    async def get(self):
        session = await get_session(self)
        session['last_visit'] = str(datetime.utcnow())
        last_visit = session['last_visit']
        text = 'Last visited: {}'.format(last_visit)
        return dict(text='login Aiohttp!, {}'.format(text))

    async def post(self):
        data = await self.post()
        login = data['login']
        password = data['password']

        session = await get_session(self)
        session['user'] = {'login': login}

        location = self.app.router['index'].url_for()
        return web.HTTPFound(location=location)


class Signup(web.View):

    async def get(self):
        return web.Response(text='signup Aiohttp!')
