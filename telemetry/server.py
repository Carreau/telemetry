import time
import zmq

import logging

log = logging.getLogger()

context = zmq.Context()
socket = context.socket(zmq.PULL)
socket.bind("tcp://*:5555")


from collections import defaultdict

agregate = defaultdict(lambda:defaultdict(lambda:0))

import time

while True:
    #  Wait for next request from client
    env_message = socket.recv()
    env = env_message[:8]
    message = env_message[9:]
    agregate[env][message] += 1
    count = agregate[env][message]
    # log roughly only 0.1 of the time we've seen this value so far
    if count % int('1'+'0'*(len(str(count))-1)) == 0:
        log.critical("Received request: %s : %s" , message, count)
