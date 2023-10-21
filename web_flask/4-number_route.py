#!/usr/bin/python3
'''starts a Flask web application'''

from flask import Flask

exu = Flask(__name__)


@exu.route('/', strict_slashes=False)
def acc():
    return 'Hello HBNB!'


@exu.route('/hbnb', strict_slashes=False)
def hbnb():
    return 'HBNB'


@exu.route('/c/<text>', strict_slashes=False)
def c_is_fun(text):
    return 'C ' + text.replace('_', ' ')


@exu.route('/python/<text>', strict_slashes=False)
def python_is_cool(text='is cool'):
    return 'Python ' + text.replace('_', ' ')


@exu.route('/number/<int:n>', strict_slashes=False)
def is_number(n):
    return "{:d} is a number".format(n)


if __name__ == '__main__':
    exu.run(host='0.0.0.0', port='5000')
