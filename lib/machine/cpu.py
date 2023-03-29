import asyncio
import re
import os
from os.path import exists
from os.path import join as path

from .utils import get, ls, ls_glob, basename, parse_temperature


# CPU thermal zone names for various devices
cpu_thermals = [
	"coretemp",		# Most desktop computers
	"cpu_thermal",	# Raspberry Pis
	"k10temp",		# My AMD-based terminal
]


# Those sensors' values are not divided by 1000
non_division_sensors = [
	"cpu_thermal",	# Raspberry Pis
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
				if key.startswith("Package id"): continue
	
			current = get(f"{zone}_input", isint=True)
			meltdown = get(f"{zone}_crit", isint=True)
			divide = sensor_name not in ["cputhermal"]
			temps[key] = [parse_temperature(current, divide=divide), parse_temperature(meltdown, divide=divide)]

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

		for line in cpu_info.split("\n"):
			if "model name" in line:
				cpu_model = re.sub(".*model name.*:", "", line, 1).strip()
			if "cache size" in line:
				cache_size = int(re.sub(".*cache size.*:", "", line, 1).strip().split(" ")[0])
			if "cpu cores" in line:
				cores = int(re.sub(".*cpu cores.*:", "", line, 1).strip())

		return {
			"model": cpu_model,
			"cache": cache_size,
			"cores": cores
		}



def get_stat():
	with open('/proc/stat') as f:
		fields = [float(column) for column in f.readline().strip().split()[1:]]
		f.close()

	return fields


def find_cpu_thermal():
	location = "/sys/class/hwmon"

	for sensor in ls(location):
		name = get(path(sensor, "name"))
		if name not in cpu_thermals:
			continue

		return {
			"location": sensor,
			"name": name
		}


def cpu_freq_helper(cpu_path: str, type: str):
	freq = get(path(cpu_path, f"cpufreq/scaling_{type}_freq"), isint=True)

	if not freq:
		freq = get(path(cpu_path, f"cpufreq/cpuinfo_{type}_freq"), isint=True)

	try:
		freq = round(freq / 1000)
	except:
		freq = None

	return freq
