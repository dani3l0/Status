# Status

**but it's v2**

**First version is under `old` branch**

This is a new, rewritten version of Status. Expect bugs and missing features, as not everything might be implemented yet.

🔨 Code is more flexible and organized

🖥️ UI is refreshed, providing new cool features with even more pleasant look

ℹ️ Providing more information in better, more readable way

⚖️ Improved stability

**[Check the demo!](https://status-ksk5.onrender.com/)** (but give it a while to load as Render suspends unused apps)

Works on desktop computers, VMs, Raspberry Pis, and some virtual isolated environments like Render :>


## Installation

Nothing has changed here.

```
# Clone the repo
git clone https://github.com/dani3l0/Status && cd Status

# Install dependenc(y)
pip install -r requirements.txt

# Run!
python3 status.py
```

**Status should be available on [localhost:9090](http://localhost:9090)**


## Configuration

This changed a lot. Configuration is now easier and more functional.

Status can now be configured via **configuration file**, **environment variables** and **command line arguments**.

**The importance of them is in the following order:**

1. **Command line arguments** - the most important and will override everything.

2. **environment variables** - will override configuration file.

3. **configuration file** - the least important, overrides default configuration only.

**Keys naming**

Config keys are named slightly differently under different ways of configuration. Understand it by example:

| JSON config file key                       | Environment variable                      | Command line argiment
|--------------------------------------------|-------------------------------------------|------------------------------------------------|
| `server.port`                              | `STATUS_SERVER_PORT`                      | `--server-port`                                |
| `server.address`                           | `STATUS_SERVER_ADDRESS`                   | `--server-address`                             |
| `misc.debug`                               | `STATUS_MISC_DEBUG`                       | `--misc-debug`                                 |

**Also, check `--help` for more information.**

Soon I'm gonna write a better README
