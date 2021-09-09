from json import JSONDecodeError
from typing import Callable

from aiohttp import web, web_exceptions as wex
from aiohttp.web import Request, Response, RouteTableDef

from src import _log_record, bot_api, exceptions, settings
from src.log import logger


routes = RouteTableDef()


@routes.post('/log')
async def handle_log_msg(request: Request) -> Response:
    """ The route handle log records with the structure:
    {
        "logger_name": str,
        "logger_level": 'DEBUG', 'INFO' etc,
        "record_date": string with iso format,
        "where": str, where the exception occurred. Optional,
        "message": what should be shown as a log data.
    }
    """
    json_resp = await request.json()
    log_record = _log_record.parse_response(json_resp)

    await bot_api.send_log_record(log_record)

    return Response(text='Log record processed')


@web.middleware
async def error_middleware(request: Request,
                           handler: Callable):
    try:
        if (response := await handler(request)).status == 200:
            return response

        status = response.status
        msg = f"{response.text}; {response.reason}; {response.body}"
    except (wex.HTTPException, JSONDecodeError,
            exceptions.InvalidJSONFormat) as e:
        logger.error(repr(e))
        raise wex.HTTPBadRequest(reason=repr(e))
    except Exception as e:
        logger.error(repr(e))
        msg, status = repr(e), 500

    if status != 500:
        raise wex.HTTPBadRequest(reason=msg)
    raise wex.HTTPInternalServerError(reason=msg)


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
