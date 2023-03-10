<img src="screenshots/status.png" alt="Status" width="600"/>

## 🧐 What is it?

A simple server monitoring app written in Python.
Designed to be lightweight, simple and pleasant to use.

It utilizes virtual file systems (/proc, /sys) for resource measurements, for maximum speed & simplicity.

[Live demo](https://status-ksk5.onrender.com/) (give it a while to load, as Render suspends unused apps)

## 🚀 Installation

**A Linux machine is required.**
Tested on some AMD and Intel computers.
Moreover, seems to work fine on Raspberry Pis.
Virtual isolated environments might cause unexpected behaviour.

<u>The best way is to host it on **bare metal**</u>.

### Clone the repo:

```
git clone https://github.com/dani3l0/Status && cd Status
```

### Install required dependenc(y):

```
pip install -r requirements.txt
```

### And, simply run the app:

```
python3 status.py
```

**Status is now served on [localhost:9000](http://localhost:9000).**


## 📝 Configuration

Set `STATUS_CONFIG_PATH` environment variable for custom config path.

**Note:** `config.json` file is created under first run!

| Section   | Key                 | Description                                                                                                                                                                                                                                                                                         |
|-----------|---------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `server`  | `port`              | HTTP(S) port Status is listening on                                                                                                                                                                                                                                                                 |
| `server`  | `bind_address`      | Address Status is listening on                                                                                                                                                                                                                                                                      |
| `server`  | `domain`            | Domain name, enables HTTPS. By default, uses Let's Encrypt certificates from _/etc/letsencrypt_ (example: `minipc.mydomain.com`)                                                                                                                                                                    |
| `server`  | `tls_cert_path`     | Custom TLS certificate path for manual HTTPS configuration.                                                                                                                                                                                                                                         |
| `server`  | `tls_key_path`      | Custom TLS private key path for manual HTTPS configuration.                                                                                                                                                                                                                                         |
| `machine` | `network_interface` | A network interface name we want to be measured. `auto` for auto-detection, otherwise set a desired interface name, like `eno1`                                                                                                                                                                     |
| `machine` | `hwmon_sensor`      | **Source of temperature values.** It's a hwmon sensor name for temperature measurement.<br>Some devices might have different sensor name (like Raspberry Pis having `cpu_thermal`).<br>**If you see unknown temperatures**, check `cat /sys/class/hwmon/*/name` for list of available sensor names. |
| `machine` | `auto_fs`           | Auto-detect mounted disks & partitions                                                                                                                                                                                                                                                              |
| `machine` | `disks`             | Describes which disks/partitions we want to have listed, **please see below**.<br>Ignored when `auto_fs` is set to `true`.                                                                                                                                                                          |
| `misc`    | `aiohttp_quiet`     | Disables HTTP library exceptions and debugging stuff. For **development**, please use `false`.                                                                                                                                                                                                      |


### 💾 Disks (manual config, works only when `auto_fs` is set to `false`)

**Here's the single disk definition from default config:**

```
"Primary": ["/", "folder", "#F66"]
```

`Primary` - desired disk/partition name to be shown in app

`/` - path of the target filesystem

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

## ⬇️ Updating

This will reset your local changes and download the latest version from here.

**Go to your working directory and type the following:**

```
git reset --hard
git pull
```
