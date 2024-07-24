#!/usr/bin/python3
"""
Fabric script generates .tgz archive of all in web_static/ using func 'do_pack'
Usage: fab -f 1-pack_web_static.py do_pack
"""
from fabric.api import local
from strftime import time


def do_pack():
    """Generate .tgz archive of web_static/ folder"""
    time_format = strftime("%Y%M%d%H%M%S")
    try:
        local("mkdir -p versions")
        filename = "versions/web_static_{}.tgz".format(time_format)
        local("tar -cvzf {} web_static/".format(filename))
        return filename
    except Exception as e:
        return None
