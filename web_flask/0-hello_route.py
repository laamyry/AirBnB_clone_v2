#!/usr/bin/python3
'''starts a Flask web application'''
from flask import Flask

exu = Flask(__name__)


@exu.route('/')
def hello():
    return 'Hello HBNB!'


if __name__ == '__main__':
    exu.run(host='0.0.0.0', port=5000, debug=True)
