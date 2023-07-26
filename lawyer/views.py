from aiohttp import web
import aiohttp_jinja2
from datetime import datetime

from services import MessageService
from email_ import build_message, build_body


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
        await MessageService(self.request.app['db']).create_message(**data)
        email = data['email']
        name = data['name']
        phone = data['phone']
        text = data['text']
        to_addr = self.request.app['config']['smtp']['messages_email']
        from_addr = self.request.app['config']['smtp']['user']
        email_body = build_body(
            email=email,
            name=name,
            phone=phone,
            text=text
        )
        email_message = build_message(
            subject="New problem.",
            from_addr=email,
            body=email_body
        )
        self.request.app['smtp_server'].sendmail(
            from_addr=from_addr,
            to_addrs=[to_addr],
            msg=email_message
        )
        message = "(Message is sent successfully)"
        context.update(message=message)
        return context


@aiohttp_jinja2.template("services.html")
@extends
async def services(request):
    return {"title": "Services"}


@aiohttp_jinja2.template("works.html")
@extends
async def works(request):
    return {"title": "Works"}
