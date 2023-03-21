import os

from .utils import get, colors


class Storage:
	@staticmethod
	def get_usage():
		filesystems = {}
		i = 0
		mounts = get("/etc/mtab").split("\n")
		for mount in mounts:
			if mount.startswith("/dev/"):
				line = mount.split(" ")
				stuff = nice_path(line[1])
				filesystems[stuff[0]] = [line[1], stuff[1], colors[i % len(colors)]]
				i += 1
		for fs in filesystems:
			stat = os.statvfs(filesystems[fs][0])
			filesystems[fs] = {
				"icon": filesystems[fs][1],
				"color": filesystems[fs][2],
				"total": round(stat.f_blocks * stat.f_bsize / 1000 * 1024),
				"available": round(stat.f_bavail * stat.f_bsize / 1000 * 1024)
			}
		return filesystems


def nice_path(path):
	if path == "/":
		return ["OS", "settings"]
	elif path.startswith("/boot"):
		return ["Boot", "flag"]
	return [path.split("/")[-1].title(), "folder"]
