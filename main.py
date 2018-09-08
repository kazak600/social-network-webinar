import logging
from aiohttp import web

from routes.base import setup_routes
from config.common import BaseConfig


def main():
    app = web.Application()
    setup_routes(app)
    app['config'] = BaseConfig
    logging.basicConfig(level=logging.DEBUG)
    web.run_app(app)


if __name__ == '__main__':
    main()
