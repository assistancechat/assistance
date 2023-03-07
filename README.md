# Assistance

The Python AI assistance library.

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
sudo supervisorctl restart chat-api
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

### Add a user to admin

Create password in ipython:

```ipython
import secrets
secrets.token_urlsafe()
```

```bash
htpasswd /etc/apache2/.htpasswd username
htpasswd /etc/apache2/.phirho-htpasswd username
```
