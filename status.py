import ssl
from time import time
from aiohttp import web
from machine import Machine


########################################################################################################################

# Runs the default config with 1 root partition, 'eno1' as network interface and 'coretemp' as hwmon sensor
stat = Machine()

# Custom setup, uncomment below lines and adjust values on your own
# stat = Machine(
#     {  # Filesystems: "Name": ["mount point", "icon name (https://fonts.google.com/icons)", "icon color"]
#         "System": ["/", "folder", "#F66"],
#         "Home": ["/home", "folder", "#F66"],
#         "Backups": ["/mnt/backups", "backup", "#F66"]
#     },
#     iface="eno1",  # Default network interface
#     hwmon_sensor="coretemp"  # Sensor name to read temperatures from. Names can be found at /sys/class/hwmon/*/name
# )

domain = None  # Set this to get Secure HTTP with Let's Encrypt certificates.
port = 9000  # Port on which app will be served
host = "0.0.0.0"  # Address on which app will be served

########################################################################################################################


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
app.add_routes(routes)

ssl_context = None
if domain:
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_dir = f"/etc/letsencrypt/live/{domain}"
    ssl_context.load_cert_chain(f"{ssl_dir}/fullchain.pem", f"{ssl_dir}/privkey.pem")

web.run_app(app, host=host, port=port, ssl_context=ssl_context)
