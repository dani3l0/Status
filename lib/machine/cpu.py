import asyncio
import re
import os

from .utils import get, ls, basename, temp_val


cpu_thermals = [
	"coretemp",		# Most desktop computers
	"cputhermal",	# Raspberry Pis
	"k10temp"		# My AMD-based terminal
]


class CPU:
	def __init__(self):
		self.cpu_model = self.get_cpu_model()

	async def get_full_info(self):
		return {
			"model": self.cpu_model,
			"utilisation": (await self.get_utilisation()),
			"temperatures": self.get_temperatures(),
			"frequencies": self.get_frequencies(),
			"count": self.get_cores()
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

	@staticmethod
	def get_temperatures():
		sensor = find_cpu_thermal()
		temps = []
		temps_meltdown = []
		labels = []
		for entry in ls(sensor):
			f = basename(entry)
			if f.startswith("temp"):
				if f.endswith("_input"):
					temps.append(temp_val(get(entry, isint=True)))
				elif f.endswith("_crit"):
					temps_meltdown.append(temp_val(get(entry, isint=True)))
				elif f.endswith("_label"):
					labels.append(get(entry).title())
		nice = {x[0]: [x[1], x[2]] for x in zip(labels, temps, temps_meltdown) if "Package" not in x[0]}
		return nice

	@staticmethod
	def get_frequencies():
		freqs = {}
		for entry in ls("/sys/devices/system/cpu/"):
			f = basename(entry)
			if f.startswith("cpu") and f[-1:].isnumeric():
				freq = cpu_freq_helper(entry, "cur")
				min_freq = cpu_freq_helper(entry, "min")
				max_freq = cpu_freq_helper(entry, "max")
				base_freq = get(os.path.join(entry, "cpufreq/base_frequency"), isint=True)
				freqs[f] = {
					"now": round(freq / 1000),
					"min": round(min_freq / 1000),
					"base": round(base_freq / 1000),
					"max": round(max_freq / 1000)
				}
		return freqs

	@staticmethod
	def get_cores():
		return os.cpu_count()

	@staticmethod
	def get_cpu_model():
		cpu_info = get("/proc/cpuinfo")
		cpu_model = "Unknown"
		for line in cpu_info.split("\n"):
			if "model name" in line:
				cpu_model = re.sub(".*model name.*:", "", line, 1).strip()
				break
			elif "Model" in line:
				cpu_model = re.sub(".*Model.*:", "", line, 1).strip()
				break
		return cpu_model


def get_stat():
	with open('/proc/stat') as f:
		fields = [float(column) for column in f.readline().strip().split()[1:]]
		f.close()
	return fields


def find_cpu_thermal():
	thermals = {}
	location = "/sys/class/hwmon"

	for sensor in ls(location):
		name = get(os.path.join(sensor, "name"))
		if name not in cpu_thermals:
			continue
		return sensor


def cpu_freq_helper(cpu_path: str, type: str):
	freq = None
	try:
		freq = get(os.path.join(cpu_path, f"cpufreq/scaling_{type}_freq"), isint=True)
	except FileNotFoundError:
		freq = get(os.path.join(cpu_path, f"cpufreq/cpuinfo_{type}_freq"), isint=True)
	return freq
