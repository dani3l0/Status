import argparse

CONFIG_DEFAULT = {
	"server": {
		"port": {
			"value": 9090,
			"short": "p",
			"desc": "web port Status is listening on"
		},
		"address": {
			"value": "0.0.0.0",
			"short": "a",
			"desc": "address Status is listening on"
		}
	}
}

class Config:
	def __init__(self):
		parser = argparse.ArgumentParser(description="Status - simple & convenient way to monitor your machine.")

		for section in CONFIG_DEFAULT:
			for key in CONFIG_DEFAULT[section]:
				a = CONFIG_DEFAULT[section][key]
				value = a["value"]
				desc = a["desc"]
				short = f"-{a['short']}"

				if a['short']: parser.add_argument(short, f"--{section}-{key}", metavar="\b", type=type(value), help=desc)
				else: parser.add_argument(f"--{section}-{key}", metavar="\b", type=type(value), help=desc)

		self.config = vars(parser.parse_args())

		for section in CONFIG_DEFAULT:
			for key in CONFIG_DEFAULT[section]:
				value = CONFIG_DEFAULT[section][key]["value"]
				var_name = f"{section}_{key}"
				if self.config[var_name] == None:
					self.config[var_name] = value


	def get(self, section, key):
		try:
			var_name = f"{section}_{key}"
			return self.config[var_name]
		except KeyError:
			return None
