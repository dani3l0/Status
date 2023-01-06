import ssl
import json
from time import time
from aiohttp import web
from machine import Machine


DEFAULT_CONFIG = {
    "server": {
        "port": 9000,
        "bind_address": "0.0.0.0",
        "domain": None,
        "tls_cert_path": None,
        "tls_key_path": None
    },
    "machine": {
        "network_interface": "auto",
        "hwmon_sensor": "coretemp",
        "auto_fs": True,
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
    CONFIG = DEFAULT_CONFIG
    conf = open("config.json", "w")
    conf.write(json.dumps(CONFIG, indent=4))
    conf.close()



def conf(section, key):
    try:
        return CONFIG[section][key]
    except KeyError:
        return DEFAULT_CONFIG[section][key]


stat = Machine(
    conf("machine", "disks"),
    conf("machine", "auto_fs"),
    conf("machine", "network_interface"),
    conf("machine", "hwmon_sensor")
)

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

    except (web.HTTPInternalServerError, web.HTTPForbidden, web.HTTPNotFound):
        raise web.HTTPFound(location="/")


routes.static("/", static)
app = web.Application(middlewares=[redirector])
app.logger.manager.disable = 100 * conf("misc", "aiohttp_quiet")
app.add_routes(routes)

ssl_context = None
if conf("server", "domain"):
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_dir = f"/etc/letsencrypt/live/{conf('server', 'domain')}"

    pubkey = conf("server", "tls_cert_path")
    if not pubkey:
        pubkey = f"{ssl_dir}/fullchain.pem"
    privkey = conf("server", "tls_key_path")
    if not privkey:
        privkey = f"{ssl_dir}/privkey.pem"

    ssl_context.load_cert_chain(pubkey, privkey)

web.run_app(app, host=conf("server", "bind_address"), port=conf("server", "port"), ssl_context=ssl_context)
