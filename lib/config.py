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
			"desc": "custom path to TLS certificate, used if domain is set"
		},
		"ssl_key": {
			"value": None,
			"desc": "custom path to TLS private key, used if domain is set"
		},
		"enable_cors": {
			"value": False,
			"desc": "enable access to API via third-party origins (domain, scheme or port)"
		},
	},
	"machine": {
		"hide_boot_partition": {
			"value": True,
			"desc": "hide partitions under /boot in Storage menu"
		},
		"custom_storage": {
			"value": False,
			"short": "cs",
			"no_value": True,
			"desc": "Disable automatic detection of mounted storage devices, use custom mount points from config"
		},
		"storage": {
			"value": {
				"OS": "/",
				"Files": "/home",
				"Logs": "/var/log"
			}
		},
		"enable_storage_blacklist": {
			"value": False,
			"short": "sb",
			"no_value": True,
			"desc": "Enable filesystem blacklist"
		},
		"storage_blacklist": {
			"value": []
		}
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
				conf_map[f"{section}_{key}"] = f"{section}.{key}"
				if "desc" not in a:
					continue

				if "short" not in a:
					a["short"] = None
				no_value = a["no_value"] if "no_value" in a else False
				action = "count" if no_value else None
				k = key.replace("_", "-")

				if a['short']: arg = parser.add_argument(f"-{a['short']}", f"--{section}-{k}", action=action)
				else: arg = parser.add_argument(f"--{section}-{k}", action=action)
				arg.help = a["desc"]
				if not action: arg.metavar = key.upper()

		parser.add_argument("-c", "--config", help="custom path to config file")
		parser.add_argument("--no-config", action="count", help="ignore config files; don't read nor save them")

		# Here the nightmare begins
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
				if var_name not in self.config or self.config[var_name] == None:
					self.config[var_name] = value


		if self.config["misc_debug"]:
			print("Debug is enabled.")


	def get(self, section, key):
		try:
			var_name = f"{section}_{key}"
			return self.config[var_name]
		except KeyError:
			return None


global config
config = Config()
