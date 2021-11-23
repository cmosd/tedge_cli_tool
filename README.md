# tedge_cli_tool

simple tool for building and syncing deb thin-edge files with a known host.


# how to install

```
pipenv shell

python install.py
```

this will create a `tedge_cli` executable (yes with no .py). You can then add the path of this repository to `$PATH` so you can run it from anywhere.

```
PATH="$PATH:path/to/tedge_cli_tool/"
```

# usage

```shell
tedge_cli build -a armhf -b feature/CIT-659/restart-device-local-operation -n remote-pi --release
```

