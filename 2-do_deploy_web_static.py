#!/usr/bin/python3
''''Fabric script (based on the file 1-pack_web_static.py) that distributes
an archive to your web servers, using the function do_deploy:'''
from fabric.api import env, run, put, local
import os
from datetime import datetime as date


def do_pack():
    '''Compress before sending'''
    try:
        now = date.now()
        times = now.strftime("%Y%m%d%H%M%S")
        arc_name = "versions/web_static_{}.tgz".format(times)
        local("mkdir -p versions")
        local("tar -czf {} web_static".format(arc_name))
        return arc_name
    except Exception as exc:
        return None


env.hosts = ['100.26.132.85', '100.26.167.53']


def do_deploy(archive_path):
    '''Distributing archive to the web server.'''
    if not os.path.exists(archive_path):
        return False

    try:
        archive_name = os.path.basename(archive_path)
        rem_path = "/tmp/{}".format(archive_name)
        rel_path = "/data/web_static/releases/{}/".format(archive_name[:-4])

        put(archive_path, rem_path)
        run("mkdir -p {}".format(rel_path))
        run("tar -xzf {} -C {}".format(rem_path, rel_path))
        run("rm {}".format(rem_path))
        run("mv {}web_static/* {}".format(rel_path, rel_path))
        run("rm -rf {}web_static".format(rel_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(rel_path))
        print("New version deployed!")

    except Exception as exc:
        print("Error: {}".format(exc))
        return False
