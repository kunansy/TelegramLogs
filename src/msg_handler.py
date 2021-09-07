from aiohttp import web
from aiohttp.web import Request, Response, RouteTableDef

from src import settings, bot_api


routes = RouteTableDef()


@routes.post('/log')
async def handle_log_msg(request: Request) -> Response:
    try:
        log_record = await request.json()
    except Exception as e:
        print(e)
        return Response(status=400)

    await bot_api.send_message(str(log_record))

    return Response(text='Log record processed')


async def error_middleware(request: Request,
                           handler: Any):
    try:
        if (response := await handler(request)).status == 200:
            return response

        status = response.status
        msg = f"{response.text}; {response.reason}; {response.body}"
    except Exception as e:
        msg, status = repr(e), 500

    return web.json_response({
        'error': msg,
        'status': status
    })


app = web.Application(middlewares=[error_middleware])
app.add_routes(routes)


async def start_app():
    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(
        runner,
        host=settings.LOG_MSG_HANDLER_HOST,
        port=settings.LOG_MSG_HANDLER_PORT
    )
    await site.start()
