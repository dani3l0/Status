import traceback
from aiohttp import web
from lib.machine import Machine


machine = Machine()


async def get_status():
    info = await machine.get_full_info()
    return info


routes = web.RouteTableDef()


@routes.get("/")
async def index(request):
    return web.FileResponse("static/index.html")


@routes.get("/api/status")
async def api(request):
    try:
        return web.json_response(await get_status())
    except:
        return web.Response(text=traceback.format_exc(), status=500)


@web.middleware
async def redirector(request, handler):
    try:
        resp = await handler(request)
        return resp

    except (web.HTTPInternalServerError, web.HTTPForbidden, web.HTTPNotFound):
        raise web.HTTPFound(location="/")


routes.static("/", "static")
app = web.Application(middlewares=[redirector])
# app.logger.manager.disable = 100 * True
app.add_routes(routes)

# ssl_context = None
# ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
# ssl_dir = f"/etc/letsencrypt/live/{conf('server', 'domain')}"
#
# pubkey = conf("server", "tls_cert_path")
# if not pubkey:
#     pubkey = f"{ssl_dir}/fullchain.pem"
# privkey = conf("server", "tls_key_path")
# if not privkey:
#     privkey = f"{ssl_dir}/privkey.pem"
#
# ssl_context.load_cert_chain(pubkey, privkey)

web.run_app(app, host="0.0.0.0", port=9090)
