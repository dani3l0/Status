import ssl
import json
from time import time
from aiohttp import web
from machine import Machine


CONFIG = {
    "server": {
        "port": 9000,
        "bind_address": "0.0.0.0",
        "domain": None
    },
    "machine": {
        "network_interface": "eno1",
        "hwmon_sensor": "coretemp",
        "disks": {
            "Primary": ["/", "folder", "#F66"]
        }
    },
    "misc": {
        "aiohttp_quiet": True
    }
}


try:
    CONFIG = json.loads(open("config.json").read())
except FileNotFoundError:
    conf = open("config.json", "w")
    conf.write(json.dumps(CONFIG, indent=4))
    conf.close()


stat = Machine(CONFIG["machine"]["disks"], CONFIG["machine"]["network_interface"], CONFIG["machine"]["hwmon_sensor"])

stat_cache = {}
stat_cache_updated = 0
static = "static"


async def get_status():
    global stat_cache, stat_cache_updated
    update = time()
    if stat_cache_updated + .5 <= update:
        stat_cache_updated = update
        stat_cache = {
            "cpu": await stat.get_cpu(),
            "loadavg": stat.get_loadavg(),
            "memory": stat.get_memory(),
            "storage": stat.get_storage(),
            "net": stat.get_net(),
            "host": stat.get_host()
        }
    return stat_cache


routes = web.RouteTableDef()


@routes.get("/")
async def index(request):
    return web.FileResponse(f"{static}/index.html")


@routes.get("/api/status")
async def api(request):
    return web.json_response(await get_status())


@web.middleware
async def redirector(request, handler):
    try:
        resp = await handler(request)
        return resp

    except web.HTTPInternalServerError or web.HTTPForbidden:
        raise web.HTTPFound(location="/")


routes.static("/", static)
app = web.Application(middlewares=[redirector])
app.logger.manager.disable = 100 * CONFIG["misc"]["aiohttp_quiet"]
app.add_routes(routes)

ssl_context = None
if CONFIG["server"]["domain"]:
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_dir = f"/etc/letsencrypt/live/{CONFIG['server']['domain']}"
    ssl_context.load_cert_chain(f"{ssl_dir}/fullchain.pem", f"{ssl_dir}/privkey.pem")

web.run_app(app, host=CONFIG["server"]["bind_address"], port=CONFIG["server"]["port"], ssl_context=ssl_context)
