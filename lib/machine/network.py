from .utils import get


class Network:

	@staticmethod
	def get_net():
		interface = get_default_iface_name_linux()
		path = f"/sys/class/net/{interface}"

		try:
			rx = get(f"{path}/statistics/rx_bytes", isint=True)
			tx = get(f"{path}/statistics/tx_bytes", isint=True)
		except FileNotFoundError:
			rx = 0
			tx = 0

		try:
			speed = get(f"{path}/speed", isint=True)
		except (OSError, FileNotFoundError):
			speed = -1

		return {
			"interface": interface,
			"speed": speed,
			"rx": rx,
			"tx": tx
		}



def get_default_iface_name_linux():
	route = "/proc/net/route"
	interface = None
	with open(route) as f:
		for line in f.readlines():
			try:
				iface, dest, _, flags, _, _, _, _, _, _, _, = line.strip().split()
				if dest != '00000000' or not int(flags, 16) & 2:
					continue
				interface = iface
				break
			except:
				continue
	return interface
