#!/usr/bin/python3
'''distributes an archive to your web servers, using the function do_deploy:'''

from fabric.api import env, put, run, local
from fabric.decorators import task
import os
from datetime import datetime as date

env.hosts = ['100.26.132.85', '100.26.167.53']


@task
def do_pack():
    format_date = date.now().strftime('%Y%m%d%H%M%S')
    mkdir = "mkdir -p versions"
    path = "versions/web_static_{}.tgz".format(format_date)
    print("Packing web_static to {}".format(path))
    if local("{} && tar -cvzf {} web_static".format(mkdir, path)).succeeded:
        return path
    return None


@task
def do_deploy(archive_path):
    try:
        if not os.path.exists(archive_path):
            return False
        with_exi = os.path.basename(archive_path)
        not_exi, ext = os.path.splitext(with_exi)
        deploy_path = "/data/web_static/releases/"
        put(archive_path, "/tmp/")
        run("rm -rf {}{}/".format(deploy_path, not_exi))
        run("mkdir -p {}{}/".format(deploy_path, not_exi))
        run("tar -xzf /tmp/{} -C {}{}/".format(with_exi, deploy_path, not_exi))
        run("rm /tmp/{}".format(with_exi))
        run("mv {0}{1}/web_static/* {0}{1}/".format(deploy_path, not_exi))
        run("rm -rf {}{}/web_static".format(deploy_path, not_exi))
        run("rm -rf /data/web_static/current")
        run("ln -s {}{}/ /data/web_static/current".format(deploy_path, not_exi))
        print("New version deployed!")
        return True
    except Exception:
        return False
