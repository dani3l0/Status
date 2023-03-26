document.addEventListener("DOMContentLoaded", () => {
	loadBackButtons()
	update()
	setInterval(update, 1500)
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

function update() {
	let xhr = new XMLHttpRequest()
	xhr.open("GET", "api/status")
	xhr.onload = function() {parseData(this)}
	xhr.send()
}

let data_prev
function parseData(resp) {
	let data = JSON.parse(resp.responseText)
	if (!data_prev) data_prev = data
	updateCPU(data.cpu)
	updateMem(data.memory)
	updateStorage(data.storage)
	updateNet(data_prev.network, data.network)
	updateHost(data.host)
	data_prev = data
}