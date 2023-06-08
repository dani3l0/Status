## Requirements

To run Status you need to have a **:penguin: Linux machine** with :snake: `python3` and `python3-pip`. App is aimed to be lightweight, so **:potato: weak hardware is not a limitation**.

On x64 devices app will use **~30MB of physical memory** and literally no CPU power.


## How to run

It's easy, but I'm working to make it even easier. Moreover, there are multiple ways of doing it.

### Bare-metal

**:heavy_check_mark: Recommended.** Status has access to all virtual filesystems in your OS, which means more information and most reliable values.

```
# Clone the repo
git clone https://github.com/dani3l0/Status && cd Status

# Install required modules
pip3 install -r requirements.txt

# Run Status!
python3 status.py
```

### Docker

**:warning: Unusable for now.** See [#1](../../issues/1). There are problems with volumes and symlinks.

```
# Clone the repo
git clone https://github.com/dani3l0/Status && cd Status

# Build & run app
docker-compose up -d
```


App should be available on [localhost:9090](http://localhost:9090).

## Tips

- :memo: Status creates its config in a directory you are currently working in
- :no_entry_sign: Use `--no-config` to skip config creation
- :question: Check `--help` for more detailed information
