## Options

Status can be configured in multiple ways:

1. :desktop_computer: **Command line arguments** - the most important and will override everything.

2. :national_park: **Environment variables** - will override configuration file.

3. :memo: **Configuration file** - the least important, overrides default configuration only.

It's good not to mix them (but you can). Use `--help` for more information.


## Keys naming

Config keys are named slightly differently under different ways of configuration. Look at the table:

|                | in JSON config      | Environment variable        | Command line argument |
|----------------|---------------------|-----------------------------|-----------------------|
| **The rule**   | `{section}.{key}`   | `STATUS_{SECTION}_{KEY}`    | `--{section}-{key}`   |
| **Example #1** | `server.port`       | `STATUS_SERVER_PORT`        | `--server-port`       |
| **Example #2** | `server.address`    | `STATUS_SERVER_ADDRESS`     | `--server-address`    |
| **Example #3** | `misc.debug`        | `STATUS_MISC_DEBUG`         | `--misc-debug`        |

Command line offers `--config` (or `-c`) to set custom config location.

Running Status with `--no-config` will neither read nor write any configuration file. Will override the above.