document.addEventListener("DOMContentLoaded", () => {
	loadBackButtons()
	update()
	setInterval(update, 2000)
})

function loadBackButtons() {
	let buttons = getClasses("back")
	for (button of buttons) {
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

function parseData(resp) {
	let data = JSON.parse(resp.responseText)
	console.log(data.host)
	updateCPU(data.cpu)
	updateMem(data.memory)
	updateStorage(data.storage)
	updateHost(data.host)
}