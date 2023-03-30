import argparse
import json
from os import environ


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
			"short": None,
			"desc": "custom path to TLS certificate, used if domain is set"
		},
		"ssl_key": {
			"value": None,
			"short": None,
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

		parser.add_argument("-c", "--config", help="custom path to config file")
		parser.add_argument("--no-config", action="count", help="ignore config files: don't read/save them")
		self.config = vars(parser.parse_args())

		# Read config from environment variables
		ENV = {}
		for key in environ:
			if key.startswith("STATUS_"):
				var_name = key.replace("STATUS_", "").lower()
				if var_name in self.config and self.config[var_name] == None:
					self.config[var_name] = environ[key]

		# Read config from file
		path = self.config["config"]
		path = path if path else "config.json"
		if not self.config["no_config"] and path:
			try:
				f = open(path, "r").read()
				print("Config files are not implemented yet.")

			except FileNotFoundError:
				with open(path, "w") as file:
					print("Config file not found.")
					print(f"Saving current configuration to {path}...")
					file.write(json.dumps(self.config, indent=4))
					file.close()

		# Fallback values from default config
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
