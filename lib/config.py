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
			"no_value": True,
			"desc": "more debugging, show core exceptions"
		},
	}
}


class Config:
	def __init__(self):
		parser = argparse.ArgumentParser(description="Status - simple and lightweight system monitoring tool for small homeservers.")
		conf_map = {}

		# Read config from arguments
		for section in CONFIG_DEFAULT:
			for key in CONFIG_DEFAULT[section]:
				a = CONFIG_DEFAULT[section][key]
				no_value = a["no_value"] if "no_value" in a else False
				action = "count" if no_value else None
				k = key.replace("_", "-")

				if a['short']: arg = parser.add_argument(f"-{a['short']}", f"--{section}-{k}", action=action)
				else: arg = parser.add_argument(f"--{section}-{k}", action=action)
				arg.help = a["desc"]
				if not action: arg.metavar = key.upper()

				conf_map[f"{section}_{key}"] = f"{section}.{key}"

		parser.add_argument("-c", "--config", help="custom path to config file")
		parser.add_argument("--no-config", action="count", help="ignore config files; don't read nor save them")
		self.config = vars(parser.parse_args())


		# Read config from environment variables
		ENV = "STATUS"
		for key in environ:
			if key.startswith(f"{ENV}_"):
				var_name = key.replace(f"{ENV}_", "").lower()
				if var_name in self.config and self.config[var_name] == None:
					self.config[var_name] = environ[key]


		# Read config from file
		path = self.config["config"]
		path = path if path else "config.json"
		if not self.config["no_config"] and path:
			try:
				config_file = json.loads(open(path, "r").read())
				for section in config_file:
					for key in config_file[section]:
						CONFIG_DEFAULT[section][key]["value"] = config_file[section][key]

			except FileNotFoundError:
				config_file = {}
				for entry in conf_map:
					e = conf_map[entry].split(".")
					section = e[0]
					key = e[1]
					if section not in config_file:
						config_file[section] = {}
					config_file[section][key] = CONFIG_DEFAULT[section][key]["value"]

				with open(path, "w") as file:
					print(f"Config file not found. Saving default configuration to {path}...")
					file.write(json.dumps(config_file, indent=4))
					file.close()


		# Fallback values from default config
		for section in CONFIG_DEFAULT:
			for key in CONFIG_DEFAULT[section]:
				value = CONFIG_DEFAULT[section][key]["value"]
				var_name = f"{section}_{key}"
				if self.config[var_name] == None:
					self.config[var_name] = value


		if self.config["misc_debug"]:
			print("Debug is enabled.")


	def get(self, section, key):
		try:
			var_name = f"{section}_{key}"
			return self.config[var_name]
		except KeyError:
			return None
