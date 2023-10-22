#!/usr/bin/python3
'''starts a Flask web application:'''
from flask import Flask, render_template as templates
from models import *
from models import storage
exu = Flask(__name__)


@exu.route('/states_list', strict_slashes=False)
def states_list():
    states = sorted(list(storage.all("State").values()), key=lambda x: x.name)
    return templates('7-states_list.html', states=states)


@exu.teardown_appcontext
def teardown_db(exception):
    storage.close()


if __name__ == '__main__':
    exu.run(host='0.0.0.0', port='5000')
