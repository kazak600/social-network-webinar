import hashlib
import aiohttp_jinja2

from aiohttp import web
from aiohttp_session import get_session

from models.user import User


class Index(web.View):

    @aiohttp_jinja2.template('index.html')
    async def get(self):
        conf = self.app['config']
        session = await get_session(self)
        user = {}
        if 'user' in session:
            user = session['user']
        return dict(conf=conf, user=user)


class Login(web.View):

    @aiohttp_jinja2.template('login.html')
    async def get(self):
        return dict()

    async def post(self):
        data = await self.post()
        email = data['email']
        password = data['password']

        user = await User.get_user(db=self.app['db'], email=email)
        if user.get('error'):
            location = self.app.router['login'].url_for()
            return web.HTTPFound(location=location)

        if user['password'] == hashlib.sha256(password.encode('utf8')).hexdigest():
            session = await get_session(self)
            session['user'] = user

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
            # todo: show error on ui!
            location = self.app.router['signup'].url_for()
            return web.HTTPFound(location=location)

        location = self.app.router['login'].url_for()
        return web.HTTPFound(location=location)


class Logout(web.View):

    async def get(self):
        session = await get_session(self)
        del session['user']

        location = self.app.router['login'].url_for()
        return web.HTTPFound(location=location)
