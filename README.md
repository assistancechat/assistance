# Assistance

The Python AI assistance library.

## Installation

### WASI Python Sandbox

Install `wasmedge`:

```
curl -sSf https://raw.githubusercontent.com/WasmEdge/WasmEdge/master/utils/install.sh | bash
```

Download `python.wasm`:

```
wget https://github.com/assistancechat/assistance/releases/download/python-wasm/python-3.11.1-wasmedge.wasm -O ~/.assistance/wasm/python.wasm
```

Test that it works:

```
wasmedge \
  --env PYTHONPATH=/assistance:/assistance/.venv/lib/python3.11/site-packages \
  --dir /assistance:$HOME/git/assistance \
  ~/.assistance/wasm/python.wasm
```

Acknowledgment to https://wasmlabs.dev/articles/python-wasm32-wasi/ where much
of the above was inspired from.

## Notes

### Dev Tooling

- [VSCode](https://code.visualstudio.com/)

### Server Hosting

First time setup of supervisor:

```bash
sudo ln -s $HOME/git/assistance/dev/server/supervisor.conf /etc/supervisor/conf.d/assistance.conf
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl status assistance
```

Restart supervisorctl

```bash
sudo supervisorctl restart assistance
```

### Poetry Python version

```bash
poetry env use $(which python)
```

### Sync data locally

```bash
rsync -r assistance:~/.assistance/* ~/.assistance/
rsync -r server:~/.assistance/* ~/.assistance/
```
