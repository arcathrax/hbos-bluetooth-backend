# hbos-bluetooth-backend

This is the backend that will receive the bluetooth settings
from the *hbos-frontend* and will adjust the config file accordingly.

## Setup
Install the following packages:
- flask
- flask-cors

**For archlinux**
```bash
sudo pacman -Syyu python-flask python-flask-cors
```

## Run the server
```bash
flask --app main.py run
```
