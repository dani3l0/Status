import os
import platform
import re
import asyncio

colors = ["#F26", "#78F", "#0D8", "#FB0", "#96F", "#F56", "#0CB", "#F60"]


def getval(path, isint=False):
    val = open(path, "r").read().rstrip()
    return int(val) if isint else val


def grep(contents, keyword):
    for line in contents.split("\n"):
        if keyword in line:
            return re.sub(r'[^0-9]', '', line)


def temp_val(raw_value):
    if (len(str(raw_value))) >= 4:
        raw_value /= 1000

    return raw_value


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


def nice_path(path):
    if path == "/":
        return ["OS", "settings"]
    elif path == "/boot" or path.startswith("/boot/"):
        return ["Boot", "flag"]
    return [path.split("/")[-1].title(), "folder"]


class Machine:
    def __init__(self, filesystems=None, auto_fs=True, iface="auto", hwmon_sensor="coretemp"):
        if filesystems is None:
            filesystems = {"Primary": ["/", "folder", "#F66"]}
        self.cpu_model = "Unknown"
        self.iface_auto = iface == "auto"
        self.fs_auto = auto_fs
        cpuinfo = getval("/proc/cpuinfo")
        for line in cpuinfo.split("\n"):
            if "model name" in line:
                self.cpu_model = re.sub(".*model name.*:", "", line, 1).strip()
        self.arch = platform.architecture()
        self.hwmon_sensor = hwmon_sensor
        self.filesystems = filesystems
        self.iface = iface

    async def get_cpu(self):
        with open('/proc/stat') as f:
            fields = [float(column) for column in f.readline().strip().split()[1:]]
            f.close()
        await asyncio.sleep(0.5)
        with open('/proc/stat') as f:
            fields2 = [float(column) for column in f.readline().strip().split()[1:]]
            f.close()
        last_idle, last_total = fields[3], sum(fields)
        idle, total = fields2[3], sum(fields2)
        idle_delta, total_delta = idle - last_idle, total - last_total
        utilisation = 1.0 - idle_delta / total_delta
        cores = os.cpu_count()
        path = "/sys/class/hwmon"
        hwmon = [f"{path}/{x}" for x in os.listdir(path)]
        core_temps = []
        max_temps = []
        temp_id = 0
        for sensor in hwmon:
            if getval(f"{sensor}/name") == self.hwmon_sensor:
                while True:
                    try:
                        temp_id += 1
                        coretemp = getval(f"{sensor}/temp{temp_id}_input", True)
                        max_temp = getval(f"{sensor}/temp{temp_id}_crit", True)
                        core_temps.append(temp_val(coretemp))
                        max_temps.append(temp_val(max_temp))
                    except FileNotFoundError:
                        break

        cpu_cur_freqs = []
        cpu_min_freqs = []
        cpu_max_freqs = []
        cpuid = 0
        while True:
            try:
                path = f"/sys/devices/system/cpu/cpu{cpuid}/cpufreq"
                current_freq = getval(f"{path}/scaling_cur_freq", True)
                min_freq = getval(f"{path}/cpuinfo_min_freq", True)
                max_freq = getval(f"{path}/cpuinfo_max_freq", True)
                cpu_cur_freqs.append(current_freq)
                cpu_min_freqs.append(min_freq)
                cpu_max_freqs.append(max_freq)
                cpuid += 1
            except FileNotFoundError:
                break

        return {
            "model": self.cpu_model,
            "cores": cores,
            "cur_freq": cpu_cur_freqs,
            "min_freq": cpu_min_freqs,
            "max_freq": cpu_max_freqs,
            "utilisation": utilisation,
            "core_temp": core_temps,
            "meltdown": max_temps,
        }

    @staticmethod
    def get_loadavg():
        res = getval("/proc/loadavg")
        res = res.split(" ")[:3]
        res = [float(i) for i in res]
        return res

    @staticmethod
    def get_memory():
        meminfo = getval("/proc/meminfo")
        total = grep(meminfo, "MemTotal:")
        available = grep(meminfo, "MemAvailable:")
        cached = grep(meminfo, "Cached:")
        swap_total = grep(meminfo, "SwapTotal:")
        swap_available = grep(meminfo, "SwapFree:")

        return {
            "total": int(total),
            "available": int(available),
            "cached": int(cached),
            "swap_total": int(swap_total),
            "swap_available": int(swap_available),
        }

    def get_storage(self):
        if self.fs_auto:
            self.filesystems = {}
            i = 0
            mounts = getval("/etc/mtab").split("\n")
            for mount in mounts:
                if mount.startswith("/dev/"):
                    line = mount.split(" ")
                    stuff = nice_path(line[1])
                    self.filesystems[stuff[0]] = [line[1], stuff[1], colors[i % len(colors)]]
                    i += 1
        filesystems = {}
        for fs in self.filesystems:
            stat = os.statvfs(self.filesystems[fs][0])
            filesystems[fs] = {
                "icon": self.filesystems[fs][1],
                "color": self.filesystems[fs][2],
                "total": round(stat.f_blocks * stat.f_bsize / 1000),
                "available": round(stat.f_bavail * stat.f_bsize / 1000)
            }
        return filesystems

    def get_net(self):
        if self.iface_auto:
            self.iface = get_default_iface_name_linux()
        path = f"/sys/class/net/{self.iface}"
        try:
            rx = getval(f"{path}/statistics/rx_bytes", True)
            tx = getval(f"{path}/statistics/tx_bytes", True)
        except FileNotFoundError:
            rx = 0
            tx = 0
        try:
            speed = getval(f"{path}/speed", True)
        except OSError:
            speed = -1
        return {
            "interface": self.iface,
            "speed": speed,
            "rx": rx,
            "tx": tx
        }

    @staticmethod
    def get_host():
        uptime = float(getval("/proc/uptime").split(" ")[0])
        os_release = getval("/etc/os-release").split("\n")
        operating_system = "Unknown"
        for line in os_release:
            if line.startswith("PRETTY_NAME"):
                operating_system = line.split('"')[1]
        hostname = getval("/etc/hostname")
        pid = str(os.getpid())
        stat = getval(f"/proc/{pid}/status")
        app_memory = grep(f"{stat}", "VmRSS:")
        return {
            "uptime": uptime,
            "os": operating_system,
            "hostname": hostname,
            "app_memory": app_memory
        }
