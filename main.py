import base64
import logging
import aiohttp_jinja2
import jinja2
from aiohttp import web

from aiohttp_session import setup, get_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from motor.motor_asyncio import AsyncIOMotorClient

from routes.base import setup_routes, setup_static_routes
from config.common import BaseConfig
from models.user import User


async def current_user_ctx_processor(request):
    session = await get_session(request)
    user = None
    is_anonymous = True
    if 'user' in session:
        user_id = session['user']['_id']
        user = await User.get_user_by_id(db=request.app['db'], user_id=user_id)
        if user:
            is_anonymous = not bool(user)

    return dict(current_user=user, is_anonymous=is_anonymous)


def main():
    app = web.Application(debug=True)

    secret_key = base64.urlsafe_b64decode(BaseConfig.secret_key)
    setup(app, EncryptedCookieStorage(secret_key))

    aiohttp_jinja2.setup(
        app,
        loader=jinja2.PackageLoader(package_name='main', package_path='templates'),
        context_processors=[current_user_ctx_processor])

    setup_routes(app)
    setup_static_routes(app)

    app['config'] = BaseConfig
    app['db'] = getattr(AsyncIOMotorClient(), BaseConfig.database_name)

    logging.basicConfig(level=logging.DEBUG)
    web.run_app(app)


if __name__ == '__main__':
    main()
