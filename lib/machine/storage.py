import os
import shutil

from .utils import get


class Storage:

	@staticmethod
	def get_usage():
		filesystems = {}
		mounts = get("/proc/mounts").split("\n")

		for mount in mounts:
			if mount.startswith("/dev/"):
				line = mount.split(" ")
				stuff = nice_path(line[1])
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
		return None

	return [path.split("/")[-1].title(), "folder"]
