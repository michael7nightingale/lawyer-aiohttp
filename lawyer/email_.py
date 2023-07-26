from smtplib import SMTP_SSL


async def smtp_server_context(app):
    configuration = app['config']['smtp']
    smtp_server = SMTP_SSL(
        host=configuration['host'],
        port=configuration['port']
    )
    smtp_server.ehlo()
    smtp_server.login(
        user=configuration['user'],
        password=configuration['password']
    )
    app['smtp_server'] = smtp_server

    yield

    smtp_server.close()


def build_body(name: str, email: str, phone: str, text: str) -> str:
    return (f"Name: {name}\n"
            f"Email: {email}\n"
            f"Phone: {phone}\n\n"
            f"{text}")


def build_message(from_addr: str, subject: str, body: str) -> str:
    message = """\
        From: %s
        Subject: %s

        %s
        """ % (from_addr, subject, body)
    return message
