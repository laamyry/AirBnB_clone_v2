#!/usr/bin/python3
'''distributes an archive to your web servers, using the function do_deploy:'''

from fabric.api import env, put, run, local
from fabric.decorators import task
from os.path import exists
from datetime import datetime as date

env.hosts = ['100.26.132.85', '100.26.167.53']


@task
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


@task
def do_deploy(archive_path):
    if not exists(archive_path):
        return False
    arc_file = archive_path.split('/')[-1]
    arc_name = arc_file.replace('.tgz', '')
    print(arc_file, arc_name)
    try:
        put(archive_path, '/tmp/')
        run('mkdir -p /data/web_static/releases/{}'.format(arc_name))
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}\
            '.format(arc_file, arc_name))
        run('rm -rf /tmp/{}'.format(arc_file))
        run('mv /data/web_static/releases/{}/web_static/* \
            /data/web_static/releases/{}'.format(arc_name, arc_name))
        run('rm -rf /data/web_static/releases/{}/web_static\
            '.format(arc_name))
        run('rm -rf /data/web_static/current')
        run('ln -s /data/web_static/releases/{}/ \
            /data/web_static/current'.format(arc_name))
        return True
    except Exception:
        return False
