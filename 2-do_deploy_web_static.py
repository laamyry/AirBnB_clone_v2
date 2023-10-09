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
        env.show = 'True'  # Enable command details display
        put(archive_path, '/tmp/')
        arc_file = os.path.basename(archive_path)  # Get the archive file name
        arc_file_no_ex = os.path.splitext(arc_file)[0]  # Remove the file extension
        rel_folder = "/data/web_static/releases/{}".format(arc_file_no_ex)
        run("mkdir -p {}".format(rel_folder))
        run("tar -xzf /tmp/{} -C {}".format(arc_file, rel_folder))
        run("rm /tmp/{}".format(arc_file))
        run("mv {}/web_static/* {}".format(rel_folder, rel_folder))
        run("rm -rf {}/web_static".format(rel_folder))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(rel_folder))
        print("New version deployed!")
        return True
    except Exception:
        return False
