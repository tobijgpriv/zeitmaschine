#!/usr/bin/env python3

import logging
from rpi_rf import RFDevice

logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                    format='%(asctime)-15s - [%(levelname)s] %(module)s: %(message)s',)



def turn_switch_wrapper(code,state,protocol):
    repeat=10
    pulselength=350
    gpio=17
    length=24
    turn_switch(state,repeat,pulselength,length,protocol,gpio,code)


def turn_switch(state,repeat,pulselength,length,protocol,gpio,code):
    
    
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

    turn_switch_wrapper(code,state,1)

strob(0)

#test