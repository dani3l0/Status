import os
import re

colors = ["#F26", "#78F", "#0D8", "#FB0", "#96F", "#F56", "#0CB", "#F60"]


def get(path: str, isint: bool = False):
	val = open(path, "r").read().rstrip()
	return int(val) if isint else val


def grep(contents: str, keyword: str):
	for line in contents.split("\n"):
		if keyword in line:
			return re.sub(r'[^0-9]', '', line)


def temp_val(raw_value: int):
	if (len(str(raw_value))) >= 4:
		raw_value /= 1000

	return raw_value


def ls(path: str):
	files = [os.path.join(path, f) for f in os.listdir(path)]
	return sorted(files)


def basename(path: str):
	return path.split("/")[-1]
