function updateCPU(cpu) {
	let temps = [],
		temps_meltdown = []
	for (let device in cpu.temperatures) {
		let t = cpu.temperatures[device]
		temps.push(t[0])
		temps_meltdown.push(t[1])
	}
	mkItem("cpu-list", "temp", "thermostat", "Temperature", [
		`Current: ${temps.max()} °C`,
		`Meltdown: ${temps_meltdown.min()} °C`
	])
	mkItem("cpu-list", "count", "numbers", "Core count", [
		`??? cores, ${cpu.count} thread${s(cpu.count)}`
	])
	let freq = [],
		freq_base = [],
		freq_min = [],
		freq_max = []
	for (let device in cpu.frequencies) {
		let v = cpu.frequencies[device]
		freq.push(v["now"])
		freq_base.push(v["base"])
		freq_min.push(v["min"])
		freq_max.push(v["max"])
	}
	freq_base = freq_base.max() * 1000
	freq_min = freq_min.min() * 1000
	freq_max = freq_max.max() * 1000
	mkItem("cpu-list", "speed", "speed", "Speed", [
		`${parseSize(freq_min, "Hz")} up to ${parseSize(freq_max, "Hz")}`,
		`Base: ${parseSize(freq_base, "Hz")}`
	])
	mkItem("cpu-list", "cache", "cached", "Cache size", [
		"???"
	])
}

function updateMem(mem) {
	let swap_used = mem.swap_total - mem.swap_available
	mkItem("mem-list", "swap", "extension", "Swap", [
		`Using ${parseSize(swap_used, "B")} out of ${parseSize(mem.swap_total, "B")}`,
		`${parseSize(mem.swap_available, "B")} is available`
	])
	mkItem("mem-list", "cache", "cached", "Cached", [
		parseSize(mem.cached, "B")
	])
	mkItem("mem-list", "procs", "account_tree", "Processes", [
		"???"
	])
}

function updateStorage(storage) {
	for (let disk in storage) {
		let p = storage[disk]
		let used = p.total - p.available
		mkItem("storage-list", disk, p.icon, disk, [
			`Using ${parseSize(used / 1000, "B")} out of ${parseSize(p.total / 1000, "B")}`,
			`${parseSize(p.available / 1000, "B")} is available`
		])
	}
}

function updateHost(host) {
	mkItem("host-list", "hostname", "text_format", "Device name", [
		host.hostname
	])
	mkItem("host-list", "os", "settings", "Operating system", [
		host.os
	])
	mkItem("host-list", "uptime", "timer", "Uptime", [
		mkTime(host.uptime)
	])
	mkItem("host-list", "memory", "memory", "App memory", [
		parseSize(host.app_memory, "B")
	])
	mkItem("host-list", "loadavg", "speed", "Load averages", [
		host.loadavg.join(", ")
	])
}