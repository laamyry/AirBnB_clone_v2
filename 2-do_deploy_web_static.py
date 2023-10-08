#!/usr/bin/python3
''''Fabric script (based on the file 1-pack_web_static.py) that distributes
an archive to your web servers, using the function do_deploy:'''
from fabric.api import env, run, put
import os

env.hosts = ['100.26.132.85', '	100.26.167.53']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'

def do_deploy(arc_path):
    if not os.path.exists(arc_path):
        return False

    try:
        arc_name = os.path.basename(arc_path)
        rem_path = "/tmp/{}".format(arc_name)
        rel_path = "/data/web_static/releases/{}/".format(arc_name[:4])

        put(arc_path, rem_path)
        run("mkdir -p {}".format(rel_path))
        run("tar -czf {} -C {}".format(rem_path, rel_path))
        run("rm {}".format(rem_path))
        run("mv {}web_static/* {}".format(rel_path, rel_path))
        run("rm -r {}web_static".format(rel_path))
        run("rm -r /data/web_static/current".format(rel_path))
        run("ln -s {} /data/web_static/current".format(rel_path))
        print("New version deployed!")
        return True

    except Exception as exc:
        print("Error: {}".format(exc))
        return False
