function get(id) {
	return document.getElementById(id);
}

function darken(y = true) {
	let div = get("darken");
	if (y) {
		div.classList.add("uncover");
		div.classList.add("shown");
	}
	else {
		div.classList.remove("shown");
		setTimeout(() => {
			div.classList.remove("uncover");
		}, 400);
	}
}

var EXPANDED = false;
function expand(element) {
	if (EXPANDED) return;
	darken();
	EXPANDED = true;
	get("main").classList.add("hide");
	element.classList.add("expanded");
	element.classList.add("front");
}
function hide(element, directly) {
	darken(false);
	if (!directly) element = element.parentNode.parentNode;
	get("main").classList.remove("hide");
	element.classList.remove("expanded");
	element.scrollTop = 0;
	setTimeout(() => {
		element.classList.remove("front");
		EXPANDED = false
	}, 450);
}
function hideAll() {
	let windows = document.getElementsByClassName("expanded");
	for (var i = 0; i < windows.length; i++) {
		hide(windows[i], true);
	}
}

function set(id, value) {
	return get(id).innerText = value;
}

function s(number) {
	if (number !== 1) return "s";
	return "";
}

Array.prototype.max = function() {
	return Math.max.apply(null, this);
}

Array.prototype.min = function() {
	return Math.min.apply(null, this);
}

function parseSize(value, unit="") {
	let addon = "K";
	let r_value = Math.round(value);
	if (r_value >= 1000) {
		addon = "M";
		value /= 1000;
		r_value = Math.round(r_value / 1000);
	}
	if (r_value >= 1000) {
		addon = "G";
		value /= 1000;
		r_value = Math.round(r_value / 1000);
	}
	if (r_value >= 1000) {
		addon = "T";
		value /= 1000;
		r_value = Math.round(r_value / 1000);
	}
	let fixd = 0;
	let ferst = value.toFixed(2).split(".")[0].length;
	if (ferst == 1) fixd = 2;
	else if (ferst == 2) fixd = 1;
	value = value.toFixed(fixd);
	if (!unit) unit = addon = "";
	return `${value} ${addon}${unit}`;
}

function fancyText(id, val, zero) {
	let d = get(id).classList;
	if (zero) d.add("zero");
	else d.remove("zero");
	set(id, val);
}
function mkFancyLoad(data) {
	let pp = data.loadavg[1];
	pp = 100 * pp / data.cpu.cores;
	if (pp > 100) pp = 100;
	get("main_bar").style.width = `${pp}%`;
	pp = Math.round(pp).toString();
	while (pp.length < 3) pp = "0" + pp;
	let a = pp.charAt(0);
	fancyText("main_loada", a, a == 0);
	let b = pp.charAt(1);
	fancyText("main_loadb", b, a == 0 && b == 0);
	let c = pp.charAt(2);
	fancyText("main_loadc", c, false);
}
function mkTime(seconds) {
	seconds = Math.round(seconds);
	let m = Math.floor(seconds / 60) % 60;
	let h = Math.floor(seconds / 60 / 60) % 24;
	let d = Math.floor(seconds / 60 / 60 / 24);
	let nice = "";
	if (d) nice += `${d} day${s(d)} `;
	if (h) nice += `${h} hour${s(h)} `;
	if (m) nice += `${m} minute${s(m)} `;
	if (nice == "") nice = "Seconds ago"
	return nice;
}

var disks_last;
var network_last;
var uptime_last;
function fetchData() {
	let xhr = new XMLHttpRequest();
	xhr.open("GET", "api/status");
	xhr.onload = function() {
		if (this.status !== 200) return;

		let data = JSON.parse(this.responseText);
		if (!uptime_last) uptime_last = data.host.uptime - 1;
		let delay = data.host.uptime - uptime_last;
		get("body").classList.remove("pre");

		mkFancyLoad(data);

		set("hostname", data.host.hostname);
		set("os", data.host.os);
		set("uptime", mkTime(data.host.uptime));
		set("app_memory", parseSize(data.host.app_memory, "B"));

		let cpu_temp = Math.round(data.cpu.core_temp.max() * 10) / 10;
		let cpu_meltdown = Math.round(data.cpu.meltdown.min());
		data.cpu.utilisation *= 100;
		data.cpu.utilisation += 0.25;
		let cpu_util = Math.round(data.cpu.utilisation);
		if (Math.abs(cpu_meltdown) == Infinity) {
			get("cpu_meltdown").parentNode.style.display = "none";
		}
		else {
			get("cpu_meltdown").parentNode.style.display = null;
			set("cpu_meltdown", cpu_meltdown);
		}
		if (Math.abs(cpu_temp) == Infinity) {
			set("cpu_temperature", `Unknown`);
			set("cpu_brief", `${cpu_util}%, ${parseSize(data.cpu.cur_freq.max(), "Hz")}`);
		}
		else {
			set("cpu_temperature", `${cpu_temp} °C`);
			set("cpu_brief", `${cpu_util}%, ${cpu_temp} °C`);
		}
		set("cpu_model", data.cpu.model);
		set("cpu_usage", cpu_util);
		get("cpu_bar").style.width = `${cpu_util}%`;
		set("cpu_cores", `${data.cpu.cores}`);
		set("cpu_speed", parseSize(data.cpu.cur_freq.max(), "Hz"));
		set("cpu_min_freq", parseSize(data.cpu.min_freq.max(), "Hz"));
		set("cpu_max_freq", parseSize(data.cpu.max_freq.max(), "Hz"));
		set("cpu_loadavg", data.loadavg.join(", "));

		let mem_used = data.memory.total - data.memory.available;
		let mem_pp = mem_used * 100 / data.memory.total;
		set("mem_brief", `${Math.round(mem_pp)}% of ${parseSize(data.memory.total, "B")}`);
		set("mem_total", parseSize(data.memory.total, "B"));
		set("mem_available", parseSize(data.memory.available, "B"));
		set("mem_used", parseSize(mem_used, false));
		set("mem_used_unit", parseSize(mem_used, "B").split(" ")[1]);
		get("mem_bar").style.width = `${mem_pp}%`;
		set("mem_swap_used", parseSize(data.memory.swap_total - data.memory.swap_available, "B"));
		set("mem_swap_total", parseSize(data.memory.swap_total, "B"));
		let swap_available = parseSize(data.memory.swap_available, "B") + " available";
		if (data.memory.swap_available === 0) swap_available = "Swap unavailable";
		set("mem_swap_available", swap_available);
		set("mem_cached", parseSize(data.memory.cached, "B"));

		let storage_list = get("storage_list");
		if (storage_list.innerHTML == "" | disks_last != JSON.stringify(data.storage)) {
			storage_list.innerHTML = "";
			for (let disk in data.storage) {
				let d = data.storage[disk];
				let used = d.total - d.available;
				let id = `storage_list(${disk})`;
				let item = `<div>
								<div class="icon" style="color: ${d.color}">${d.icon}</div>
								<div class="text">
									<div id="${id}_name" class="name">${disk}</div>
									<div class="value">Using <b id="${id}_used"></b> of <b id="${id}_total"></b></div>
									<div class="value"><b id="${id}_available"></b> available</div>
								</div>
							</div>`;
				storage_list.innerHTML += item;
			}
			disks_last = JSON.stringify(data.storage);
		}
		let storage_total = 0;
		let storage_available = 0;
		for (let disk in data.storage) {
			let d = data.storage[disk];
			let id = `storage_list(${disk})_`;
			storage_total += d.total;
			storage_available += d.available;
			set(id + "used", parseSize(d.total - d.available, "B"));
			set(id + "total", parseSize(d.total, "B"));
			set(id + "available", parseSize(d.available, "B"));
		}
		let storage_used = storage_total - storage_available;
		let storage_pp = 100 * storage_used / storage_total;
		set("storage_brief", `${Math.round(storage_pp)}% of ${parseSize(storage_total, "B")}`);
		get("storage_bar").style.width = `${storage_pp}%`;
		set("storage_used", parseSize(storage_used));
		set("storage_used_unit", parseSize(storage_used, "B").split(" ")[1]);
		set("storage_used_total", parseSize(storage_total, "B"));
		set("storage_available", parseSize(storage_available, "B"));

		if (!network_last || network_last.interface != data.net.interface) network_last = data.net;
		let days_passed = data.host.uptime / (60 * 60 * 24);
		let speed_down = (data.net.rx - network_last.rx) / 1000 / delay;
		let speed_up = (data.net.tx - network_last.tx) / 1000 / delay;
		let speed = speed_up + speed_down;
		let speed_bit = (speed) * 8;
		let net_pp = 0;
		if (data.net.speed > 0) {
			net_pp = 100 * speed_bit / (data.net.speed * 1000);
			set("net_link", parseSize(data.net.speed * 1000, "bit/s"));
		}
		else set("net_link", "Unavailable");
		if (data.net.interface) set("net_brief", `${parseSize(speed_bit, "bit/s")}`);
		else set("net_brief", "Unavailable");
		get("net_bar").style.width = `${net_pp}%`;
		set("net_speed", parseSize(speed_bit));
		set("net_speed_unit", parseSize(speed_bit, "bit/s").split(" ")[1]);
		set("net_speed_mb", parseSize(speed, "B/s"));
		set("net_all_all", parseSize((data.net.rx + data.net.tx) / 1000, "B"));
		set("net_all_daily", parseSize((data.net.rx + data.net.tx) / 1000 / days_passed, "B"));
		set("net_up_all", parseSize(data.net.tx / 1000, "B"));
		set("net_up_daily", parseSize(data.net.tx / 1000 / days_passed, "B"));
		set("net_down_all", parseSize(data.net.rx / 1000, "B"));
		set("net_down_daily", parseSize(data.net.rx / 1000 / days_passed, "B"));
		network_last = data.net;

		uptime_last = data.host.uptime;
	}
	xhr.send();
}
function init() {
	fetchData();
	setInterval(fetchData, 2000);
}
