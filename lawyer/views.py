from aiohttp import web
import aiohttp_jinja2
from datetime import datetime

from services import MessageService


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


class Contact(web.View):

    @aiohttp_jinja2.template("contact.html")
    @extends
    async def get(self):
        return {"title": "Contact"}

    @aiohttp_jinja2.template("contact.html")
    @extends
    async def post(self):
        context = {"title": "Contact"}
        data = await self.request.post()
        try:
            await MessageService(self.request.app['db']).create_message(**data)
            message_ = "(Message is sent successfully)"
        except Exception:
            message_ = "(Invalid data)"
        context.update(message=message_)
        return context


@aiohttp_jinja2.template("services.html")
@extends
async def services(request):
    return {"title": "Services"}


@aiohttp_jinja2.template("works.html")
@extends
async def works(request):
    return {"title": "Works"}
