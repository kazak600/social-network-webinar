import base64
import logging
import aiohttp_jinja2
import jinja2
from aiohttp import web

from cryptography import fernet
from aiohttp_session import setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from motor.motor_asyncio import AsyncIOMotorClient

from routes.base import setup_routes
from config.common import BaseConfig


def main():
    app = web.Application()

    fernet_key = fernet.Fernet.generate_key()
    secret_key = base64.urlsafe_b64decode(fernet_key)
    setup(app, EncryptedCookieStorage(secret_key))

    aiohttp_jinja2.setup(app, loader=jinja2.PackageLoader(package_name='main', package_path='templates'))

    setup_routes(app)
    app['config'] = BaseConfig
    app['db'] = getattr(AsyncIOMotorClient(), BaseConfig.database_name)

    logging.basicConfig(level=logging.DEBUG)
    web.run_app(app)


if __name__ == '__main__':
    main()
