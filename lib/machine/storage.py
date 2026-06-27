import os

from .utils import get, exists
from ..config import config


class Storage:

    @staticmethod
    def get_usage():
        filesystems = {}

        if config.get("machine", "custom_storage"):
            storage = config.get("machine", "storage")
            for item in storage:
                filesystems[item] = [storage[item], nice_path(storage[item])[1], ""]

        else:
            is_android = exists("/data/data/com.termux") or exists("/sdcard")
            if is_android:
                # On Android, just use the known reliable mount points directly
                candidates = [
                   ("/sdcard", "Internal Storage", "sd_card"),
                   ("/data/data/com.termux/files/home", "Termux Home", "terminal"),
                ]

                seen_sizes = set()
                for mountpoint, label, icon in candidates:
                    if not exists(mountpoint):
                        continue
                    try:
                        usage = os.statvfs(mountpoint)
                        size_key = (usage.f_blocks, usage.f_bsize)
                        if size_key in seen_sizes or usage.f_blocks == 0:
                            continue
                        seen_sizes.add(size_key)
                        filesystems[label] = [mountpoint, icon, ""]
                    except (PermissionError, OSError):
                        continue
            else:
                # Standard Linux mount detection
                mounts_raw = get("/proc/mounts")
                mounts = mounts_raw.split("\n") if mounts_raw else []
                listed_devices = []
                for mount in mounts:
                    if mount.startswith("/dev/"):
                        line = mount.split(" ")
                        if len(line) < 3:
                            continue
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
            except (PermissionError, OSError):
                continue

            # ext4 fs dirty-improvement to show nicely rounded storage size
            inode_overhead = 0
            if len(filesystems[fs]) > 2 and filesystems[fs][2] == "ext4":
                inode_size = 256                # Default for mkfs.ext4
                correction = 1.2
                inode_overhead = inode_size * usage.f_files * correction

            total = usage.f_bsize * usage.f_blocks + inode_overhead
            available = usage.f_bsize * usage.f_bavail

            if total == 0:
                continue

            result[fs] = {
                "icon": filesystems[fs][1],
                "total": total,
                "available": available
            }

        return result


def nice_path(path):
    if path == "/":
        return ["OS", "settings"]
    if path.startswith("/boot"):
        return ["Boot", "sprint"]
    if path.startswith("/sdcard") or path.startswith("/storage/emulated/0"):
        return ["Internal Storage", "sd_card"]
    if path.startswith("/storage/") and "emulated" not in path:
        return ["SD Card", "sd_card"]
    if "termux" in path.lower() or path.endswith("/home"):
        return ["Termux", "terminal"]
    if path.startswith("/data"):
        return ["Data", "storage"]
    if path.startswith("/mnt/"):
        return [path.split("/")[-1].title(), "folder_open"]
    return [path.split("/")[-1].title(), "folder"]
