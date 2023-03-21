function get(id) {
	return document.getElementById(id);
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
