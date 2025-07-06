#!/usr/bin/env python3

import logging
from rpi_rf import RFDevice

logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                    format='%(asctime)-15s - [%(levelname)s] %(module)s: %(message)s',)

repeat=10
pulselength=350
gpio=17


def strob(state,repeat,pulselength,length):
    protocol=1
    if state == True:
        code = 4433
    else:
        code = 4436
    
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

strob(False,repeat,pulselength,24)