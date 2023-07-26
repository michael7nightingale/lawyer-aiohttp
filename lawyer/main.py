from aiohttp import web
import aiohttp_jinja2
import jinja2

from db import pg_context
from email_ import smtp_server_context
from routes import setup_routes
from settings import config, BASE_DIR


application = web.Application()
application['config'] = config
aiohttp_jinja2.setup(
    app=application,
    loader=jinja2.FileSystemLoader(str(BASE_DIR / "lawyer" / "templates"))
)


def setup_static_routes(app: web.Application):
    app.router.add_static(
        prefix="/static",
        path=BASE_DIR / "lawyer" / "static",
        name='static'
    )


setup_routes(application)
setup_static_routes(application)

application.cleanup_ctx.append(pg_context)
application.cleanup_ctx.append(smtp_server_context)

if __name__ == '__main__':
    web.run_app(
        app=application,
    )
