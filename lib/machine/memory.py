from .utils import get, grep, ls, basename


class Memory:

	@staticmethod
	def get_usage():
		meminfo = get("/proc/meminfo")

		def safe_get_mem(key):
			val = grep(meminfo, key)
			return int(val) if val else 0

		total = safe_get_mem("MemTotal:")
		available = safe_get_mem("MemAvailable:")
		if not available:
			# Fallback for very old kernels or limited environments
			free = safe_get_mem("MemFree:")
			buffers = safe_get_mem("Buffers:")
			cached_val = safe_get_mem("Cached:")
			available = free + buffers + cached_val
		
		cached = safe_get_mem("Cached:")
		swap_total = safe_get_mem("SwapTotal:")
		swap_available = safe_get_mem("SwapFree:")

		procs = ls("/proc")
		processes = []
		for proc in procs:
			pid = basename(proc)
			if pid.isnumeric():
				processes.append(pid)

		return {
			"total": round(1024 * total / 1000),
			"available": round(1024 * available / 1000),
			"cached": round(1024 * cached / 1000),
			"swap_total": round(1024 * swap_total / 1000),
			"swap_available": round(1024 * swap_available / 1000),
			"processes": len(processes)
		}
