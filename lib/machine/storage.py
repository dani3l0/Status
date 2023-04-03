import shutil

from .utils import get
from ..config import config


class Storage:

	@staticmethod
	def get_usage():
		filesystems = {}

		if config.get("machine", "custom_storage"):
			storage = config.get("machine", "storage")
			for item in storage:
				filesystems[item] = [storage[item], nice_path(storage[item])[1]]

		else:
			mounts = get("/proc/mounts").split("\n")
			for mount in mounts:
				if mount.startswith("/dev/"):
					line = mount.split(" ")
					stuff = nice_path(line[1])
					if config.get("machine", "enable_storage_blacklist"):
						if line[1] in config.get("machine", "storage_blacklist"):
							stuff = None
					if stuff: filesystems[stuff[0]] = [line[1], stuff[1]]

		for fs in filesystems:
			usage = shutil.disk_usage(filesystems[fs][0])
			filesystems[fs] = {
				"icon": filesystems[fs][1],
				"total": usage.total,
				"available": usage.free
			}

		return filesystems



def nice_path(path):
	if path == "/":
		return ["OS", "settings"]

	elif path.startswith("/boot"):
		return ["Boot", "sprint"]

	return [path.split("/")[-1].title(), "folder"]
