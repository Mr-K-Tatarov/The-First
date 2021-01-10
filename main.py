from transport.sanic.configure_sanic import configure_app


def main():
    app = configure_app()
    app.run(
        host='localhost',
        port=8000,
    )
