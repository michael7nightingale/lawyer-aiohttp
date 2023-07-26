from aiohttp.web import Application

from views import index, contact, works, services


def setup_routes(app: Application) -> None:
    app.router.add_get("/", index, name='index')
    app.router.add_get("/contact", contact, name='contact')
    app.router.add_get("/works", works, name='works')
    app.router.add_get("/services", services, name='services')
