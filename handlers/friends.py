import aiohttp_jinja2
from aiohttp import web

from models.user import User


class FriendsView(web.View):

    @aiohttp_jinja2.template('friends.html')
    async def get(self):
        if 'user' not in self.session:
            return web.HTTPForbidden()

        friends = await User.get_user_friends_suggestions(db=self.app['db'], user_id=self.session['user']['_id'])
        return dict(friends=friends)

    async def post(self):
        return web.HTTPError()
