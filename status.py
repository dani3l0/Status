import traceback
from aiohttp import web
import ssl

from lib.config import config
from lib.machine import Machine
from lib.cache import Cache


machine = Machine()
cache = Cache()


async def get_status():
	if cache.should_update():
		info = await machine.get_full_info()
		cache.update(info)
	return cache.get()


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
app.logger.manager.disable = 100 * config.get("misc", "debug")
app.add_routes(routes)

if config.get("server", "domain"):
	ssl_context = None
	ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
	ssl_dir = f"/etc/letsencrypt/live/{config.get('server', 'domain')}"

	pubkey = config.get("server", "tls_cert_path")
	if not pubkey:
		pubkey = f"{ssl_dir}/fullchain.pem"

	privkey = config.get("server", "tls_key_path")
	if not privkey:
		privkey = f"{ssl_dir}/privkey.pem"

	ssl_context.load_cert_chain(pubkey, privkey)


web.run_app(app, host=config.get("server", "address"), port=config.get("server", "port"))
