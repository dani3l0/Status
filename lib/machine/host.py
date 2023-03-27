import os

from .utils import get, grep


class Host:

	@staticmethod
	def get_host():
		uptime = float(get("/proc/uptime").split(" ")[0])
		os_release = get("/etc/os-release").split("\n")
		operating_system = "Unknown"

		for line in os_release:
			if line.startswith("PRETTY_NAME"):
				operating_system = line.split('"')[1]

		hostname = get("/etc/hostname")
		pid = str(os.getpid())
		stat = get(f"/proc/{pid}/status")
		app_memory = grep(f"{stat}", "VmRSS:")
		loadavg = get("/proc/loadavg")
		loadavg = loadavg.split(" ")[:3]
		loadavg = [float(i) for i in loadavg]

		return {
			"uptime": uptime,
			"os": operating_system,
			"hostname": hostname,
			"app_memory": app_memory,
			"loadavg": loadavg
		}
