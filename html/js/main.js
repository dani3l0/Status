window.addEventListener("load", () => {
	update()
	hashchange()
	setInterval(update, 1500)
})

window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
	if (!localStorage.getItem("statusapp-light")) selectTheme(!platformIsDark(), false)
})

document.addEventListener("DOMContentLoaded", () => {
	loadBackButtons()
	loadThemePicker()
	try {
		let accent = localStorage.getItem("statusapp-accent")
		if (accent) selectAccent(accent, false)
		else selectAccent("red", false)
		let theme = localStorage.getItem("statusapp-light")
		if (theme) selectTheme(theme == "true", false)
		else selectTheme(!platformIsDark(), false)
	}
	catch (e) {}
})

function hashchange() {
	let hash = window.location.hash.slice(1)
	if (hash == "") hash = "main"
	goto(hash, false)
}
window.addEventListener("hashchange", hashchange)

function loadBackButtons() {
	let buttons = getClasses("back")
	for (let button of buttons) {
		button.onclick = () => {
			goBack()
		}
	}
}

function goto(target, updateHash = true) {
	if (updateHash) window.location.hash = target
	let toShow = get(target)
	let screens = getClasses("screen")
	for (screen of screens) {
		if (toShow == screen) screen.classList.remove("hidden")
		else screen.classList.add("hidden")
	}
}

function goBack() {
	window.history.back()
}

function loadThemePicker() {
	let accents = getClasses("accents")[0].children
	for (let accent of accents) {
		accent.addEventListener("click", () => {
			selectAccent(accent.className)
		})
	}
	if (!localStorage.getItem("statusapp-light")) {
		document.querySelector("#autoDarkSwitch .checkbox").classList.add("enabled")
	}
}

function selectAccent(accent, save=true) {
	accent = accent.replace("selected", "").trim()
	let available = getClasses("accents")[0].children
	let cl = document.body.classList
	for (let color of available) {
		if (color.classList.contains(accent)) {
			color.classList.add("selected")
			cl.add(accent)
		}
		else {
			color.classList.remove("selected")
			cl.remove(color.className.replace("selected", ""))
		}
	}
	if (!save) return
	try {
		localStorage.setItem("statusapp-accent", accent)
	}
	catch (e) {
		console.warn("Cookies are disabled. Settings will not be saved.")
	}
}
function selectTheme(isLight, save=true) {
	let cl = document.body.classList
	let elems = getClasses("theme")
	if (isLight) cl.add("light")
	else cl.remove("light")
	elems[0 + isLight].classList.remove("selected")
	elems[1 - isLight].classList.add("selected")
	if (!save) return
	document.querySelector("#autoDarkSwitch .checkbox").classList.remove("enabled")
	try {
		localStorage.setItem("statusapp-light", isLight)
	}
	catch (e) {
		console.warn("Cookies are disabled. Settings will not be saved.")
	}
}

function update() {
	if (document.hidden) return
	let xhr = new XMLHttpRequest()
	xhr.open("GET", "api/status")
	xhr.onload = function() {
		get("main").classList.remove("unloaded")
		parseData(this)
	}
	xhr.send()
}

let data_prev
function parseData(resp) {
	try {
		let data = JSON.parse(resp.responseText)
		if (!data_prev) data_prev = data
		updateDeviceName(data.host.hostname)
		updateCPU(data.cpu)
		updateMem(data.memory)
		updateStorage(data.storage)
		updateNet(data_prev.network, data.network)
		updateHost(data.host)
		if (data.battery) {
			updateBattery(data.battery)
		} else {
			let mainBatItem = document.getElementById("main-battery-item");
			if (mainBatItem) mainBatItem.style.display = "none";
		}
		data_prev = data
	}
	catch (e) {
		console.error(resp.responseText)
	}
}

function platformIsDark() {
	return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches
}

function setAutoTheme() {
	let node = document.getElementById("autoDarkSwitch")
	let customized = localStorage.getItem("statusapp-light")
	let shouldBeDark = platformIsDark()
	if (customized) localStorage.removeItem("statusapp-light")
	else localStorage.setItem("statusapp-light", !shouldBeDark)
	if (customized) node.querySelector(".checkbox").classList.add("enabled")
	selectTheme(!shouldBeDark, !customized)
}
