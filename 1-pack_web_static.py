#!/usr/bin/python3
'''Fabric script that generates a .tgz archive from the contents of the
web_static folder of your AirBnB Clone repo, using the function do_pack.'''

from fabric.api import local
from datetime import datetime as date


def do_pack():
    '''Compress before sending'''
    try:
        now = date.now()
        times = now.strftime("%Y%m%d%H%M%S")
        arc_name = "versions/web_static_{}.tgz"(times)
        local("mkdir -p versions")
        local("tar -czf {} web_static"(arc_name))
        return arc_name
    except Exception as exc:
        return None
