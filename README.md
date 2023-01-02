<img src="screenshots/status.png" alt="Status" width="600"/>

## What is it?

A simple server monitoring app written in Python.
Designed to be lightweight, simple and pleasant to use.

It utilizes virtual file systems (/proc, /sys) for resource measurements, for maximum speed & simplicity.


## How to host?

### Clone the repo:

```
git clone https://gitlab.com/dani3l0/status && cd status
```

### Install required dependenc(y):

```
pip install -r requirements.txt
```

### And, simply run the app:

```
python3 status.py
```

**Status is now served on [localhost:9000](localhost:9000).**


## Configuration

**Note:** `config.json` file is created under first run!

**IMPORTANT: <u>Do not delete</u> the config keys, otherwise app won't start!**

| Section   | Key                 | Description                                                                                                                                                                                                                                                                                      |
|-----------|---------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `server`  | `port`              | HTTP(S) port Status is listening on                                                                                                                                                                                                                                                              |
| `server`  | `bind_address`      | Address Status is listening on                                                                                                                                                                                                                                                                   |
| `server`  | `domain`            | Domain name, enables HTTPS with Let's Encrypt certificates (example: `minipc.mydomain.com`)                                                                                                                                                                                                      |
| `machine` | `network_interface` | A network interface name we want to be measured.                                                                                                                                                                                                                                                 |
| `machine` | `hwmon_sensor`      | **Usually, there is no need to change this.** It's a hwmon sensor name for temperature measurement. Some devices might have different sensor name (my minipc has `k10temp`).<br>**If you are getting exceptions or crashes**, check `cat /sys/class/hwmon/*/name` for list of available sensors. |
| `machine` | `disks`             | Describes which disks/partitions we want to have listed, **please see below**                                                                                                                                                                                                                    |
| `misc`    | `aiohttp_quiet`     | Disables annoying HTTP library exceptions. For **debugging**, set this to `false`.                                                                                                                                                                                                               |


### Disks

**Here's the single disk definition from default config:**

```
"Primary": ["/", "folder", "#F66"]
```

`Primary` - desired disk/partition name to be shown in app

`/` - path of the filesystem

`folder` - icon name, see [Google Icon Fonts](https://fonts.google.com/icons)

`#F66` - HEX color of the icon


**Example multi-disk config:**

```
"disks": {
    "OS": ["/", "settings", "#F66"],
    "Files": ["/home", "folder", "#68F"],
    "Backups": ["/mnt/backups", "backup", "#0D8"]
}
```

