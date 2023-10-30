import shutil
import os

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
			listed_devices = []
			for mount in mounts:
				if mount.startswith("/dev/"):
					line = mount.split(" ")
					stuff = nice_path(line[1])
					if config.get("machine", "hide_boot_partition"):
						if line[1].startswith("/boot"):
							continue
					if config.get("machine", "enable_storage_blacklist"):
						if line[1] in config.get("machine", "storage_blacklist"):
							continue
					if line[0] not in listed_devices:
						filesystems[stuff[0]] = [line[1], stuff[1], line[2]]
					listed_devices.append(line[0])

		result = {}

		for fs in filesystems:
			try:
				usage = os.statvfs(filesystems[fs][0])

			except PermissionError:
				continue

			# ext4 fs dirty-improvement to show nicely rounded storage size
			inode_overhead = 0
			if filesystems[fs][2] == "ext4":
				inode_size = 256		# Default for mkfs.ext4
				correction = 1.2
				inode_overhead = inode_size * usage.f_files * correction

			result[fs] = {
				"icon": filesystems[fs][1],
				"total": usage.f_bsize * usage.f_blocks + inode_overhead,
				"available": usage.f_bsize * usage.f_bavail
			}

		return result



def nice_path(path):
	if path == "/":
		return ["OS", "settings"]

	elif path.startswith("/boot"):
		return ["Boot", "sprint"]

	return [path.split("/")[-1].title(), "folder"]
