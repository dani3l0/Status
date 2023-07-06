import os
import re
from glob import glob


try:
	CUSTOM_ROOT_PATH = os.environ["STATUS_CUSTOM_ROOT_PATH"]
except KeyError:
	CUSTOM_ROOT_PATH = ""


def get(path: str, isint: bool = False, fallback = None):
	try:
		if os.path.exists(CUSTOM_ROOT_PATH + path):
			path = CUSTOM_ROOT_PATH + path
		val = open(path, "r").read().rstrip()
		res = int(val) if isint else val
	except (FileNotFoundError, ValueError):
		res = fallback
	return res


def grep(contents: str, keyword: str):
	for line in contents.split("\n"):
		if keyword in line:
			return re.sub(r'[^0-9]', '', line)


def temp_val(raw_value: int):
	if (len(str(raw_value))) >= 4:
		raw_value /= 1000

	return raw_value


def ls(path: str):
	if os.path.exists(CUSTOM_ROOT_PATH + path):
		path = CUSTOM_ROOT_PATH + path
	files = [os.path.join(path, f) for f in os.listdir(path)]
	return sorted(files)


def ls_glob(path: str, target: str):
	if os.path.exists(CUSTOM_ROOT_PATH + path):
		path = CUSTOM_ROOT_PATH + path
	files = glob(os.path.join(path, target))
	return sorted(files)


def basename(path: str):
	return path.split("/")[-1]


def parse_temperature(temp: int, divide: bool = True):
	if not temp: return temp
	return temp / 1000 if divide else temp