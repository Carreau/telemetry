"""
A package to collect statistics on how your library is used.

Telemetry take care of collecting (or not) statistics depending on wether
user have given consent.

We provide the decorators and function to sprinkle on your code,
in order to collect statistics.

Just choose what you wish to measure, we take care of the rest.
"""

__version__ = '0.1.dev0'


import os
import sys
import logging
import json
import functools


import zmq

address = 'tcp://localhost:5555'
context = zmq.Context()
socket = context.socket(zmq.PUSH)
socket.connect(address)


socket.send(b'starting...')


# for now just log out what we collect.


import collections

import hmac
env_id = hmac.new(sys.version.encode('ascii')).hexdigest()[:8]


def _collect(value):
    socket.send(('%s|%s' % (env_id, value)).encode('ascii'))


def collect_basic_info():
    """
    collect basic info about the system, os, python version...
    """

    s = sys.version_info
    _collect(json.dumps({'sys.version_info':tuple(s)}))
    _collect(sys.version)
    return sys.version

collect_basic_info()

def foo():
    pass

def collect_message_number(message):
    """
    collect how many time a posted message has been seen
    """
    _collect(message)


def collect_import():
    """
    collect the number of time this module is imported.
    find a way to find that.
    """
    pass

def call(function):
    """
    decorator that collect function call count.
    """
    message = 'call:%s.%s' % (function.__module__,function.__name__)
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        _collect(message)
        return function(*args, **kwargs)

    return wrapper



@call
def bar():
    pass

for i in range(20000):
    bar()
