import aiohttp_jinja2

from datetime import datetime

from aiohttp import web
from aiohttp_session import get_session

from models.user import User


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

        db = self.app['db']
        user = await User.get_user(db=db)
        document = await db.test.find_one()

        return dict(last_visit='login Aiohttp!, Last visited: {}'.format(last_visit))

    async def post(self):
        data = await self.post()
        login = data['login']
        password = data['password']

        session = await get_session(self)
        session['user'] = {'login': login}

        location = self.app.router['index'].url_for()
        return web.HTTPFound(location=location)


class Signup(web.View):

    @aiohttp_jinja2.template('signup.html')
    async def get(self):
        return dict()

    async def post(self):
        data = await self.post()
        result = await User.create_new_user(db=self.app['db'], data=data)
        if not result or result.get('error'):
            location = self.app.router['signup'].url_for()
            return web.HTTPFound(location=location)

        location = self.app.router['login'].url_for()
        return web.HTTPFound(location=location)
