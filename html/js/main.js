document.addEventListener("DOMContentLoaded", () => {
	loadBackButtons()
	update()
	setInterval(update, 1500)
	loadThemePicker()
	try {
		let accent = localStorage.getItem("statusapp-accent")
		if (accent) selectAccent(accent)
	}
	catch (e) {}
})

function loadBackButtons() {
	let buttons = getClasses("back")
	for (let button of buttons) {
		button.onclick = () => {
			goto("main")
		}
	}
}

function goto(target) {
	let toShow = get(target)
	let screens = getClasses("screen")
	for (screen of screens) {
		if (toShow == screen) screen.classList.remove("hidden")
		else screen.classList.add("hidden")
	}
}

function loadThemePicker() {
	let accents = getClasses("accents")[0].children
	for (let accent of accents) {
		accent.addEventListener("click", () => {
			selectAccent(accent.className)
			goto('main')
		})
	}
}

function selectAccent(accent) {
	document.body.className = accent
	try {
		localStorage.setItem("statusapp-accent", accent)
	}
	catch (e) {
		console.warn("Cookies are disabled. Settings will not be saved.")
	}
}

function update() {
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