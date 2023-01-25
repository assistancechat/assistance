# Assistance

The Python AI assistance library.

## Notes

### Dev Tooling

- [Pants](https://www.pantsbuild.org/docs/installation)
- [VSCode](https://code.visualstudio.com/)

### Server Hosting

To view the live logs of the running api service run:

```bash
sudo journalctl -u run-api.service -f -n 50
```

### Poetry Python version

```bash
poetry env use $(which python)
```
