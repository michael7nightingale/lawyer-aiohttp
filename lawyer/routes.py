from aiohttp.web import Application

from views import index, works, services, Contact


def setup_routes(app: Application) -> None:
    app.router.add_get("/", index, name='index')
    app.router.add_get("/works", works, name='works')
    app.router.add_get("/services", services, name='services')
    app.router.add_view("/contact", Contact, name='contact')
