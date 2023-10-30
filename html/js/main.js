window.addEventListener("load", () => {
	update()
	setInterval(update, 1500)
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
		else selectTheme(false, false)
	}
	catch (e) {}
})

window.addEventListener("hashchange", (event) => {
	let hash = window.location.hash.slice(1)
	if (hash == "") hash = "main"
	goto(hash, false)
})

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
		data_prev = data
	}
	catch (e) {
		console.error(resp.responseText)
	}
}
