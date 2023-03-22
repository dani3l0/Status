document.addEventListener("DOMContentLoaded", () => {
	loadBackButtons()
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
