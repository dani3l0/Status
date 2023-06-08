function get(id) {
	return document.getElementById(id)
}

function getClasses(name) {
	return document.getElementsByClassName(name)
}

function set(id, value) {
	return get(id).innerText = value
}

function s(number) {
	if (number !== 1) return "s"
	return ""
}

Array.prototype.max = function() {
	let arr = this
	arr = arr.filter(element => {
		return element !== null && element !== undefined
	})
	let n = Math.max.apply(null, arr)
	if (Math.abs(n) == Infinity) n = null
	return n
}

Array.prototype.min = function() {
	let arr = this
	arr = arr.filter(element => {
		return element !== null && element !== undefined
	})
	let n = Math.min.apply(null, arr)
	if (Math.abs(n) == Infinity) n = null
	return n
}

Array.prototype.addNode = function() {
	let value = arguments[0]
	let push = arguments[1]
	push = (Array.isArray(push)) ? push : [push]
	if (!push.includes(null) && !push.includes(false)) this.push(value)
}

Array.prototype.append = function() {
	let value = arguments[0]
	if (value != null) this.push(value)
}

function parseSize(value, unit="") {
	if (value == null) return null
	let addon = "K"
	let r_value = Math.round(value)
	if (r_value >= 1000) {
		addon = "M"
		value /= 1000
		r_value = Math.round(r_value / 1000)
	}
	if (r_value >= 1000) {
		addon = "G"
		value /= 1000
		r_value = Math.round(r_value / 1000)
	}
	if (r_value >= 1000) {
		addon = "T"
		value /= 1000
		r_value = Math.round(r_value / 1000)
	}
	let fixd = 0
	let ferst = value.toFixed(2).split(".")[0].length
	if (ferst == 1) fixd = 2
	else if (ferst == 2) fixd = 1
	value = value.toFixed(fixd)
	if (!unit) unit = addon = ""
	return `${value} ${addon}${unit}`
}

function mkTime(seconds) {
	seconds = Math.round(seconds)
	let m = Math.floor(seconds / 60) % 60
	let h = Math.floor(seconds / 60 / 60) % 24
	let d = Math.floor(seconds / 60 / 60 / 24)
	let nice = ""
	if (d) nice += `${d} day${s(d)} `
	if (h) nice += `${h} hour${s(h)} `
	if (m) nice += `${m} minute${s(m)} `
	if (nice == "") nice = "Less than a minute"
	return nice
}

function strToArray(str) {
	if (Number.isInteger(str)) str = str.toString()
	if (typeof(str) == "string") str = [str]
	else if (!Array.isArray(str)) str = []
	return str
}

function mkDiv(args, icon) {
	let div = document.createElement((icon) ? "i" : "div")
	if (args.id) div.id = args.id
	if (args.className) div.className = args.className
	if (args.text) {
		if (args.raw_html) div.innerHTML = args.text
		else div.innerText = args.text
	}
	return div;
}

function mkItem(target, icon, name, values, div_id) {
	values = strToArray(values)
	if (!values.length) return;
	if (!div_id) div_id = icon
	let id = `${target}-${div_id}`
	let item = get(id)
	let divs = (item) ? item.getElementsByClassName("value") : []
	if (!item || divs.length != values.length) {
		let _target = get(target)
		let _item = mkDiv({className: "item", id})
		let _icon = mkDiv({text: icon}, true)
		let _text = mkDiv({className: "text"})
		let _name = mkDiv({className: "name", text: name})
		_text.appendChild(_name)
		for (let _ of values) {
			let val = mkDiv({className: "value"})
			divs.append(val)
			_text.appendChild(val)
		}
		_item.appendChild(_icon)
		_item.appendChild(_text)
		if (item) item.innerHTML = _item.innerHTML
		else _target.appendChild(_item)
	}
	for (let i = 0; i < divs.length; i++) {
		divs[i].innerText = values[i]
	}
}

function mkBar(div, progress, value, unit, right, desc) {
	let target = get(div)
	if (!target.children.length) {
		let _text = mkDiv({className: "text"})
		let _value = mkDiv({className: "value"})
		let _unit = mkDiv({className: "unit"})
		let _right = mkDiv({className: "right"})
		let _progress = mkDiv({className: "progress"})
		let _desc = mkDiv({className: "desc"})
		_text.appendChild(_value)
		_text.appendChild(_unit)
		_text.appendChild(_right)
		target.appendChild(_text)
		target.appendChild(_progress)
		target.appendChild(_desc)
	}
	let _value = target.getElementsByClassName("value")[0]
	let _unit = target.getElementsByClassName("unit")[0]
	let _right = target.getElementsByClassName("right")[0]
	let _desc = target.getElementsByClassName("desc")[0]
	let _progress = target.getElementsByClassName("progress")[0]
	_value.innerText = value
	_unit.innerText = unit
	_right.innerText = right
	_desc.innerText = desc
	_progress.style.setProperty("--value", `${progress * 100}%`)
}