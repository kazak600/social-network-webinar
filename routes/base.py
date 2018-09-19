from handlers.base import Index, Login, Signup, Logout, PostView
from handlers.avatar import Avatar
from handlers.friends import FriendsView, MessageView

from config.common import BaseConfig


def setup_routes(app):
    app.router.add_get('/', Index.get, name='index')

    app.router.add_get('/login', Login.get, name='login')
    app.router.add_post('/login', Login.post)
    app.router.add_get('/signup', Signup.get, name='signup')
    app.router.add_post('/signup', Signup.post)
    app.router.add_get('/logout', Logout.get, name='logout')

    app.router.add_post('/save_avatar', Avatar.post, name='save_avatar')

    app.router.add_post('/add_post', PostView.post, name='add_post')

    app.router.add_get('/friends', FriendsView.get, name='friends')
    app.router.add_post('/add_friend', FriendsView.post, name='add_friend')

    app.router.add_get('/messages', MessageView.get, name='messages')
    app.router.add_post('/send_message', MessageView.post, name='send_message')


def setup_static_routes(app):
    app.router.add_static('/static/', path=BaseConfig.STATIC_DIR, name='static')
