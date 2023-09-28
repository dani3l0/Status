function updateDeviceName(deviceName) {
	set("main-device-name", deviceName)
}
function updateCPU(cpu) {
	// Temperatures
	let temps = [],
		temps_meltdown = []
	for (let device in cpu.temperatures) {
		let t = cpu.temperatures[device]
		temps.append(t[0])
		temps_meltdown.append(t[1])
	}
	let temp = temps.max()
	let meltdown = temps_meltdown.min()

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

	freq = (freq) ? parseSize(freq * 1000, "Hz") : ""


	// Add to UI
	let _values_cpu = []
	_values_cpu.addNode(`${Math.round(cpu.utilisation * 100)}%`)
	_values_cpu.addNode(freq, freq != "")
	_values_cpu.addNode(`${temp} °C`, temp)
	set("main-cpu", _values_cpu.join(", "))

	mkBar("cpu-bar",
		cpu.utilisation, Math.round(cpu.utilisation * 100), "%",
		(freq) ? `Speed: ${freq}` : "",
		cpu.model
	)

	let _values_temp = []
	_values_temp.addNode(`Current: ${Math.round(temp* 10) / 10} °C`, temp)
	_values_temp.addNode(`Meltdown: ${Math.round(meltdown* 10) / 10} °C`, meltdown)
	mkItem("cpu-list", "thermostat", "Temperature", _values_temp)

	mkItem("cpu-list", "numbers", "Core count", [
		`${cpu.cores} core${s(cpu.cores)}, ${cpu.count} thread${s(cpu.count)}`
	])

	let _values_freq = []
	_values_freq.addNode(`${parseSize(freq_min * 1000, "Hz")} up to ${parseSize(freq_max * 1000, "Hz")}`, (freq_min && freq_max))
	_values_freq.addNode(`Base: ${parseSize(freq_base * 1000, "Hz")}`, freq_base)
	mkItem("cpu-list", "speed", "Speed", _values_freq)

	mkItem("cpu-list", "cached", "Cache size", parseSize(cpu.cache / 1024 * 1000, "B"))
}


function updateMem(mem) {
	// Parse data
	let swap_used = mem.swap_total - mem.swap_available
	let mem_used = mem.total - mem.available
	let m = parseSize(mem_used, "B").split(" ")


	// Add to UI
	set("main-mem", `Using ${m.join(" ")} out of ${parseSize(mem.total, "B")}`)

	mkBar("mem-bar",
		mem_used / mem.total, m[0], m[1],
		`${parseSize(mem.total, "B")} in total`,
		`${parseSize(mem.available, "B")} is available`
	)

	let _values_swap = []
	_values_swap.addNode(`Using ${parseSize(swap_used, "B")} out of ${parseSize(mem.swap_total, "B")}`, mem.swap_total != 0)
	_values_swap.addNode(`${parseSize(mem.swap_available, "B")} is available`, mem.swap_total != 0)
	_values_swap.addNode(`Unavailable`, mem.swap_total == 0)
	mkItem("mem-list", "extension", "Swap", _values_swap)

	mkItem("mem-list", "cached", "Cached", parseSize(mem.cached, "B"))
	mkItem("mem-list", "account_tree", "Processes", mem.processes)
}

var storage_last = []
function updateStorage(storage) {
	let all_total = 0
	let all_used  = 0
	for (let disk in storage) {
		let p = storage[disk]
		let used = p.total - p.available

		// Add to disks list
		mkItem("storage-list", p.icon, disk, [
			`Using ${parseSize(used / 1000, "B")} out of ${parseSize(p.total / 1000, "B")}`,
			`${parseSize(p.available / 1000, "B")} is available`
		], disk)

		all_used += used
		all_total += p.total
	}

	// Clean unused disks
	if (Object.keys(storage_last).length > 0) {
		for (let last_disk in storage_last) {
			if (!(last_disk in storage)) {
				document.getElementById(`storage-list-${last_disk}`).remove()
			}
		}
	}

	let all_free = all_total - all_used
	let s = parseSize(all_used / 1000, "B").split(" ")


	// Add to UI
	set("main-storage", `Using ${s.join(" ")} out of ${parseSize(all_total / 1000, "B")}`)

	mkBar("storage-bar",
		all_used / all_total, s[0], s[1],
		`${parseSize(all_total / 1000, "B")} in total`,
		`${parseSize(all_free / 1000, "B")} is available`
	)

	storage_last = storage
}


function updateNet(net_last, net) {
	let rx_diff = net.rx - net_last.rx
	let tx_diff = net.tx - net_last.tx
	let rx_speed = rx_diff / 1.5 / (1000 / 8)
	let tx_speed = tx_diff / 1.5 / (1000 / 8)

	set("main-network", parseSize(rx_speed + tx_speed, "bit/s"))

	set("net-up-speed", parseSize(tx_speed, "bit/s"))
	set("net-up-speed-bytes", parseSize(tx_speed / 8, "B/s"))
	set("net-down-speed", parseSize(rx_speed, "bit/s"))
	set("net-down-speed-bytes", parseSize(rx_speed / 8, "B/s"))

	let netspeed = (net.speed != -1) ? parseSize(net.speed * 1000, "bit/s") : "Unknown" 
	mkItem("net-list", "speed", "Connection speed", netspeed)

	mkItem("net-list", "arrow_upward", "Upload", [
		`${parseSize(net.tx / 1000, "B")} since boot`
	])
	mkItem("net-list", "arrow_downward", "Download", [
		`${parseSize(net.rx / 1000, "B")} since boot`
	])
}


function updateHost(host) {
	set("main-host", host.os)
	mkItem("host-list", "text_format", "Device name", host.hostname)
	mkItem("host-list", "settings", "Operating system", host.os)
	mkItem("host-list", "timer", "Uptime", mkTime(host.uptime))
	mkItem("host-list", "memory", "App memory", parseSize(host.app_memory, "B"))
	mkItem("host-list", "speed", "Load averages", host.loadavg.join(", "))
}
