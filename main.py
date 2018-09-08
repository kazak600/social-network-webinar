import base64
import logging
from aiohttp import web

from cryptography import fernet
from aiohttp_session import setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage


from routes.base import setup_routes
from config.common import BaseConfig


def main():
    app = web.Application()

    fernet_key = fernet.Fernet.generate_key()
    secret_key = base64.urlsafe_b64decode(fernet_key)
    setup(app, EncryptedCookieStorage(secret_key))

    setup_routes(app)
    app['config'] = BaseConfig
    logging.basicConfig(level=logging.DEBUG)
    web.run_app(app)


if __name__ == '__main__':
    main()
