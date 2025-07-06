#!/usr/bin/env python3

import logging
from rpi_rf import RFDevice

logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                    format='%(asctime)-15s - [%(levelname)s] %(module)s: %(message)s',)



def turn_switch_wrapper(code,protocol):
    repeat=10
    pulselength=350
    gpio=17
    length=24
    turn_switch(repeat,pulselength,length,protocol,gpio,code)


def turn_switch(repeat,pulselength,length,protocol,gpio,code):
    
    
    rfdevice = RFDevice(gpio)
    rfdevice.enable_tx()
    rfdevice.tx_repeat = repeat
    logging.info(str(code) +
             " [protocol: " + str(protocol) +
             ", pulselength: " + str(pulselength) +
             ", length: " + str(length) +
             ", repeat: " + str(rfdevice.tx_repeat) + "]")

    rfdevice.tx_code(code, protocol, pulselength, length)
    rfdevice.cleanup()


def strob(state):
    if state == 1:
        code = 4433
    else:
        code = 4436
    protocol = 1

    turn_switch_wrapper(code,protocol)

def drei(state):
    if state == 1:
        code = 5201
    else:
        code = 5204
    protocol = 1

    turn_switch_wrapper(code,protocol)

def vier(state):
    if state == 1:
        code = 1361
    else:
        code = 1364
    protocol = 1

    turn_switch_wrapper(code,protocol)

def drehlicht(state):
    if state == 1: 
        code=5755988
    else:
        code=5755985
    
    protocol = 2

    turn_switch_wrapper(code,protocol)

def alles_aus():
    strob(0)
    drehlicht(0)
    drei(0)
    vier(0)

def alles_an():
    strob(1)
    drehlicht(1)
    drei(1)
    vier(1)

def zeitreise():
    strob(1)
    drehlicht(1)
    drei(1)
    vier(1)

def standardbeleuchtung():
    strob(1)
    drehlicht(0)
    drei(0)
    vier(0)
