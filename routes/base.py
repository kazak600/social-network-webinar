from handlers.base import Index, Login, Signup, Logout
from handlers.avatar import Avatar

from config.common import BaseConfig


def setup_routes(app):
    app.router.add_get('/', Index.get, name='index')
    app.router.add_get('/login', Login.get, name='login')
    app.router.add_post('/login', Login.post)
    app.router.add_get('/signup', Signup.get, name='signup')
    app.router.add_post('/signup', Signup.post)
    app.router.add_get('/logout', Logout.get, name='logout')
    app.router.add_post('/save_avatar', Avatar.post)


def setup_static_routes(app):
    app.router.add_static('/static/', path=BaseConfig.static_dir, name='static')
