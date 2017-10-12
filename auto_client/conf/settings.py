import os

BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PLUGIN_ITEMS = {
    "nic": "src.plugins.nic.Nic",
    "disk": "src.plugins.disk.Disk",
    "memory": "src.plugins.memory.Memory",
}

API = "http://192.168.1.101:8080/api/server.html"

TEST = True

MODE = "AGENT" # AGENT/SSH/SALT

SSH_USER = "root"
SSH_PORT = 22
SSH_PWD = "sdf"