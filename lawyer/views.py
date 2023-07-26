import aiohttp_jinja2
from datetime import datetime


def get_base_context() -> dict:
    return {
        "year": datetime.now().year
    }


def extends(func):
    async def inner(request):
        context = await func(request)
        context.update(get_base_context())
        return context
    return inner


@aiohttp_jinja2.template("index.html")
@extends
async def index(request):
    return {"title": "Home"}


@aiohttp_jinja2.template("contact.html")
@extends
async def contact(request):
    return {"title": "Contact", }


@aiohttp_jinja2.template("services.html")
@extends
async def services(request):
    return {"title": "Services"}


@aiohttp_jinja2.template("works.html")
@extends
async def works(request):
    return {"title": "Works"}
