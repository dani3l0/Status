function updateCPU(cpu) {
	// Temperatures
	let temps = [],
		temps_meltdown = []
	for (let device in cpu.temperatures) {
		let t = cpu.temperatures[device]
		temps.append(t[0])
		temps_meltdown.append(t[1])
	}
	let temp = Math.round(temps.max() * 10) / 10
	let meltdown = Math.round(temps_meltdown.min() * 10) / 10

	let _values_temp = []
	_values_temp.addNode(`Current: ${temp} °C`, temp != null)
	_values_temp.addNode(`Meltdown: ${meltdown} °C`, meltdown != null)
	mkItem("cpu-list", "temp", "thermostat", "Temperature", _values_temp)

	// Cores
	mkItem("cpu-list", "count", "numbers", "Core count", [
		`${cpu.cores} core${s(cpu.cores)}, ${cpu.count} thread${s(cpu.count)}`
	])

	// Frequencies
	let freq = [],
		freq_base = [],
		freq_min = [],
		freq_max = []
	for (let device in cpu.frequencies) {
		let v = cpu.frequencies[device]
		freq.append(v["now"])
		freq_base.append(v["base"])
		freq_min.append(v["min"])
		freq_max.append(v["max"])
	}
	freq = freq.max()
	freq_base = freq_base.max()
	freq_min = freq_min.min()
	freq_max = freq_max.max()

	let _values_freq = []
	_values_freq.addNode(`${parseSize(freq_min, "Hz")} up to ${parseSize(freq_max, "Hz")}`, freq_min != null && freq_max != null)
	_values_freq.addNode(`Base: ${parseSize(freq_base, "Hz")}`, freq_base != null)
	mkItem("cpu-list", "speed", "speed", "Speed", _values_freq)

	// Cache
	mkItem("cpu-list", "cache", "cached", "Cache size", [
		parseSize(cpu.cache, "B")
	])

	// Progressbar & overview
	mkBar("cpu-bar",
		cpu.utilisation, Math.round(cpu.utilisation * 100), "%",
		`Speed: ${parseSize(freq, "Hz")}`,
		cpu.model
	)

	set("main-cpu", `${Math.round(cpu.utilisation * 100)}%, ${parseSize(freq, "Hz")}, ${temps.max()} °C`)
}

function updateMem(mem) {
	let swap_used = mem.swap_total - mem.swap_available
	let mem_used = mem.total - mem.available
	mkItem("mem-list", "swap", "extension", "Swap", [
		`Using ${parseSize(swap_used, "B")} out of ${parseSize(mem.swap_total, "B")}`,
		`${parseSize(mem.swap_available, "B")} is available`
	])

	mkItem("mem-list", "cache", "cached", "Cached", [
		parseSize(mem.cached, "B")
	])

	mkItem("mem-list", "procs", "account_tree", "Processes", [
		mem.processes
	])

	let m = parseSize(mem_used, "B").split(" ")
	mkBar("mem-bar",
		mem_used / mem.total, m[0], m[1],
		`${parseSize(mem.total, "B")} in total`,
		`${parseSize(mem.available, "B")} is available`
	)

	set("main-mem", `Using ${m.join(" ")} out of ${parseSize(mem.total, "B")}`)
}

function updateStorage(storage) {
	let all_total = 0
	let all_used  = 0
	for (let disk in storage) {
		let p = storage[disk]
		let used = p.total - p.available
		mkItem("storage-list", disk, p.icon, disk, [
			`Using ${parseSize(used / 1000, "B")} out of ${parseSize(p.total / 1000, "B")}`,
			`${parseSize(p.available / 1000, "B")} is available`
		])
		all_used += used
		all_total += p.total
	}

	let all_free = all_total - all_used
	let s = parseSize(all_used / 1000, "B").split(" ")
	mkBar("storage-bar",
		all_used / all_total, s[0], s[1],
		`${parseSize(all_total / 1000, "B")} in total`,
		`${parseSize(all_free / 1000, "B")} is available`
	)

	set("main-storage", `Using ${s.join(" ")} out of ${parseSize(all_total / 1000, "B")}`)
}

function updateNet(net_last, net) {
	let rx_diff = net.rx - net_last.rx
	let tx_diff = net.tx - net_last.tx
	let rx_speed = rx_diff / 1.5 / (1000 / 8)
	let tx_speed = tx_diff / 1.5 / (1000 / 8)

	set("net-up-speed", parseSize(tx_speed, "bit/s"))
	set("net-up-speed-bytes", parseSize(tx_speed / 8, "B/s"))
	set("net-down-speed", parseSize(rx_speed, "bit/s"))
	set("net-down-speed-bytes", parseSize(rx_speed / 8, "B/s"))

	mkItem("net-list", "speed", "speed", "Connection speed", [
		parseSize(net.speed * 1000, "bit/s")
	])
	mkItem("net-list", "upload", "arrow_upward", "Upload", [
		`${parseSize(net.tx / 1000, "B")} since boot`
	])
	mkItem("net-list", "download", "arrow_downward", "Download", [
		`${parseSize(net.rx / 1000, "B")} since boot`
	])
	set("main-network", parseSize(rx_speed + tx_speed, "bit/s"))
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
	set("main-host", host.os)
}