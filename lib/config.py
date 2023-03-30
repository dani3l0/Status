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
		},
		"domain": {
			"value": None,
			"short": "d",
			"desc": "domain used for auto HTTPS with Let's Encrypt certificates"
		},
		"ssl_cert": {
			"value": None,
			"short": "c",
			"desc": "custom path to TLS certificate, used if domain is set"
		},
		"ssl_key": {
			"value": None,
			"short": "k",
			"desc": "custom path to TLS private key, used if domain is set"
		},
	},
	"misc": {
		"debug": {
			"value": False,
			"short": "v",
			"action": "count",
			"desc": "more debugging, show core exceptions"
		},
	}
}

class Config:
	def __init__(self):
		parser = argparse.ArgumentParser(description="Status - simple & convenient way to monitor your machine.")

		# Read config from arguments
		for section in CONFIG_DEFAULT:
			for key in CONFIG_DEFAULT[section]:
				a = CONFIG_DEFAULT[section][key]
				value = a["value"]
				desc = a["desc"]
				short = f"-{a['short']}"
				action = a["action"] if "action" in a else None

				key = key.replace("_", "-")
				if a['short']: parser.add_argument(short, f"--{section}-{key}", action=action, help=desc)
				else: parser.add_argument(f"--{section}-{key}", action=action, help=desc)

		self.config = vars(parser.parse_args())

		# Set default values for unconfigured stuff
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
