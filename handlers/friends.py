import aiohttp_jinja2
from aiohttp import web

from models.user import User


class FriendsView(web.View):

    @aiohttp_jinja2.template('friends.html')
    async def get(self):
        if 'user' not in self.session:
            return web.HTTPForbidden()

        users = await User.get_user_friends_suggestions(db=self.app['db'], user_id=self.session['user']['_id'])
        return dict(users=users)

    async def post(self):
        if 'user' not in self.session:
            return web.HTTPForbidden()

        data = await self.post()
        await User.add_friend(db=self.app['db'], user_id=self.session['user']['_id'], friend_id=data['uid'])
        location = self.app.router['friends'].url_for()
        return web.HTTPFound(location=location)
