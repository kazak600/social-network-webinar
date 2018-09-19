import aiohttp_jinja2
from aiohttp import web

from models.user import User
from models.message import Message


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


class MessageView(web.View):

    @aiohttp_jinja2.template('messages.html')
    async def get(self):
        if 'user' not in self.session:
            return web.HTTPForbidden()

        inbox_messages = Message.get_inbox_messages_by_user(db=self.app['db'], user_id=self.session['user']['_id'])
        send_messages = Message.get_send_messages_by_user(db=self.app['db'], user_id=self.session['user']['_id'])
        return dict(inbox_messages=inbox_messages, send_messages=send_messages)

    async def post(self):
        if 'user' not in self.session:
            return web.HTTPForbidden()

        data = await self.post()
        await Message.create_message(db=self.app['db'], from_user=self.session['user']['_id'],
                                     to_user=data['to_user'], message=data['message_text'])

        location = self.app.router['index'].url_for()
        return web.HTTPFound(location=location)
