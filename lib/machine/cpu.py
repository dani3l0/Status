import asyncio
import re
import os
from os.path import join as path

from .utils import get, ls, ls_glob, basename, parse_temperature, exists

# On Android/Termux, the thermal zone name is typically "cpu-0-0-usr" or similar
# We broaden the search to cover common Qualcomm, MediaTek, and generic Android names
cpu_thermals = [
    "coretemp",        # Desktop/server
    "cpu_thermal",     # Raspberry Pi
    "k10temp",         # AMD
    "cpu-0-0-usr",     # Qualcomm Snapdragon
    "cpu0",            # Generic Android
    "cpu",             # Generic Android fallback
    "tsens_tz_sensor", # Qualcomm TSENS
]

non_division_sensors = [
    "cpu_thermal",
]

class CPU:

    def __init__(self):
        cpu_info = self.get_cpu_info()
        self.cpu_model = cpu_info["model"]
        self.cpu_cache = cpu_info["cache"]
        self.cores = cpu_info["cores"]
        self.cpu_thermal = find_cpu_thermal()

    async def get_full_info(self):
        return {
            "model": self.cpu_model,
            "utilisation": (await self.get_utilisation()),
            "temperatures": self.get_temperatures(),
            "frequencies": self.get_frequencies(),
            "count": self.get_count(),
            "cache": self.cpu_cache,
            "cores": self.cores
        }

    @staticmethod
    async def get_utilisation():
        fields = get_stat()
        await asyncio.sleep(0.5)
        fields2 = get_stat()
        last_idle, last_total = fields[3], sum(fields)
        idle, total = fields2[3], sum(fields2)
        idle_delta, total_delta = idle - last_idle, total - last_total
        if total_delta == 0:
            return 0.0
        utilisation = 1.0 - idle_delta / total_delta
        return utilisation

    def get_temperatures(self):
        if not self.cpu_thermal: return []
        thermal = self.cpu_thermal
        sensor = thermal["location"]
        sensor_name = thermal["name"]
        temps = {}

        for entry in ls_glob(sensor, "temp*_input"):
            key = basename(entry).replace("_input", "")
            zone = path(sensor, key)
            if exists(f"{zone}_label"):
                key = get(f"{zone}_label")
                if key and key.startswith("Package id"): continue

            current = get(f"{zone}_input", isint=True)
            meltdown = get(f"{zone}_crit", isint=True)
            divide = sensor_name not in ["cpu_thermal"]
            temps[key] = [parse_temperature(current, divide=divide), parse_temperature(meltdown, divide=divide)]

        # Fallback: try Android thermal_zone sysfs directly
        if not temps:
            temps = get_android_temps()

        return temps

    @staticmethod
    def get_frequencies():
        freqs = {}
        for entry in ls("/sys/devices/system/cpu/"):
            f = basename(entry)
            if f.startswith("cpu") and f[-1:].isnumeric():
                freq = cpu_freq_helper(entry, "cur")
                min_freq = cpu_freq_helper(entry, "min")
                max_freq = cpu_freq_helper(entry, "max")
                try:
                    base_freq = round(get(path(entry, "cpufreq/base_frequency"), isint=True) / 1000)
                except:
                    base_freq = None

                freqs[f] = {
                    "now": freq,
                    "min": min_freq,
                    "base": base_freq,
                    "max": max_freq
                }
        return freqs

    @staticmethod
    def get_count():
        return os.cpu_count()

    @staticmethod
    def get_cpu_info():
        cpu_model = None
        cache_size = None
        cores = 1
        cpu_info = get("/proc/cpuinfo")

        if cpu_info:
            for line in cpu_info.split("\n"):
                if "model name" in line:
                    cpu_model = re.sub(".*model name.*:", "", line, 1).strip()
                if "Hardware" in line and not cpu_model:
                    # Android fallback: grab SoC name from "Hardware" field
                    cpu_model = re.sub(".*Hardware.*:", "", line, 1).strip()
                if "cpu cores" in line:
                    try:
                        cores = int(re.sub(".*cpu cores.*:", "", line, 1).strip())
                    except ValueError:
                        pass

            if not cpu_model:
                # Last resort: processor : 0 -> count from cpuinfo
                processor_count = cpu_info.count("\nprocessor\t:")
                if processor_count > 0:
                    cpu_model = f"Android CPU ({processor_count} cores)"

        caches = [x for x in ls("/sys/devices/system/cpu/cpu0/cache") if "index" in x]
        if len(caches):
            try:
                cache_size = int(get(f"{caches[-1]}/size").rstrip("K"))
            except:
                pass

        return {
            "model": cpu_model or "Unknown Android CPU",
            "cache": cache_size,
            "cores": cores
        }


def get_stat():
    with open('/proc/stat') as f:
        fields = [float(column) for column in f.readline().strip().split()[1:]]
    return fields


def find_cpu_thermal():
    location = "/sys/class/hwmon"
    if not exists(location):
        return None

    for sensor in ls(location):
        name_path = path(sensor, "name")
        if not exists(name_path):
            continue
        name = get(name_path)
        if not name:
            continue
        # Match any known thermal name, or any that contains "cpu"
        if name in cpu_thermals or "cpu" in name.lower():
            return {
                "location": sensor,
                "name": name
            }
    return None


def get_android_temps():
    """Read thermal zones from Android's sysfs thermal interface."""
    temps = {}
    thermal_base = "/sys/class/thermal"
    if not exists(thermal_base):
        return temps

    for zone in sorted(os.listdir(thermal_base)):
        if not zone.startswith("thermal_zone"):
            continue
        zone_path = os.path.join(thermal_base, zone)
        zone_type = get(os.path.join(zone_path, "type")) or zone
        if "cpu" not in zone_type.lower() and "tsens" not in zone_type.lower():
            continue
        temp_raw = get(os.path.join(zone_path, "temp"), isint=True)
        if temp_raw is not None:
            temp_c = parse_temperature(temp_raw, divide=True)
            temps[zone_type] = [temp_c, None]
        if len(temps) >= 4:  # Show up to 4 CPU-related zones
            break

    return temps


def cpu_freq_helper(cpu_path: str, type: str):
    freq = get(path(cpu_path, f"cpufreq/scaling_{type}_freq"), isint=True)
    if not freq:
        freq = get(path(cpu_path, f"cpufreq/cpuinfo_{type}_freq"), isint=True)
    try:
        freq = round(freq / 1000)
    except:
        freq = None
    return freq
