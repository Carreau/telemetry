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


# for now just log out what we collect.
log = logging.getLogger()

# in progress, locaal counter.
import collections
_d = collections.defaultdict(lambda :0)


def _collect(value):
    _d[value] += 1
    lvalue = _d[value]
    if lvalue %10 == 0 :
        log.critical('%s -- %s',value, lvalue)


def collect_basic_info():
    """
    collect basic info about the system, os, python version...
    """

    s = sys.version_info
    _collect(json.dumps({'sys.version_info':s}))
    _collect(sys.version)

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
    message = 'call:%s.%s' % (function.__module__,function.__qualname__)
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        _collect(message)
        return function(*args, **kwargs)

    return wrapper



@call
def bar():
    pass

for i in range(200):
    bar()
