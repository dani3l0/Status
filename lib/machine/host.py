import os

from .utils import get, grep


class Host:

    @staticmethod
    def get_host():
        uptime_raw = get("/proc/uptime")
        uptime = float(uptime_raw.split(" ")[0]) if uptime_raw else 0.0

        # Android doesn't have /etc/os-release; fall back gracefully
        operating_system = "Unknown"
        for os_file in ["/etc/os-release", "/data/data/com.termux/files/usr/etc/os-release"]:
            os_release = get(os_file)
            if os_release:
                for line in os_release.split("\n"):
                    if line.startswith("PRETTY_NAME"):
                        operating_system = line.split('"')[1]
                        break
                break
        
        # If still unknown, try to detect Termux/Android
        if operating_system == "Unknown":
            if os.path.exists("/data/data/com.termux"):
                android_ver = get("/proc/version") or ""
                operating_system = "Android (Termux)"
                if "android" in android_ver.lower():
                    pass  # already set

        # Android usually doesn't expose /etc/hostname; use device hostname instead
        hostname = get("/etc/hostname") or ""
        if not hostname:
            try:
                import socket
                hostname = socket.gethostname()
            except Exception:
                hostname = "android"

        pid = str(os.getpid())
        stat = get(f"/proc/{pid}/status") or ""
        app_memory = grep(stat, "VmRSS:")

        loadavg_raw = get("/proc/loadavg")
        if loadavg_raw:
            loadavg = loadavg_raw.split(" ")[:3]
            loadavg = [float(i) for i in loadavg]
        else:
            loadavg = [0.0, 0.0, 0.0]

        return {
            "uptime": uptime,
            "os": operating_system,
            "hostname": hostname,
            "app_memory": app_memory,
            "loadavg": loadavg
        }
