# Assistance

The Python AI assistance library.

## Notes

### Dev Tooling

- [Pants](https://www.pantsbuild.org/docs/installation)
- [VSCode](https://code.visualstudio.com/)

### Server Hosting

Restart supervisorctl

```bash
sudo supervisorctl restart chat-api
```

### Poetry Python version

```bash
poetry env use $(which python)
```

### Sync data locally

```bash
rsync -r assistance:~/.assistance/* ~/.assistance/
rsync -r server:~/.assistance/* ~/.home-assistance/
```

### Add a user to admin

Create password in ipython:

```ipython
import secrets
secrets.token_urlsafe()
```

```bash
htpasswd /etc/apache2/.htpasswd username
```
