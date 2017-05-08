#!/usr/bin/python
from __future__ import print_function
import logging
import can
import re
import time

#Personal Communications between 0x90 and 0x97
pimcu=0x092
chimearb = ( 0x4 << 26) | (0x00F << 13) | pimcu

def sendchime(chime=4, delay=0x78, repeat=1):
    #000F 0xxx 86 78 05 FF 05
    # byte 4 is volume? Try me..
    # 0 = Silent
    # 1 = Blinker Tick
    # 2 = Blinker Tock
    # 3 = Blinker TickTock
    # 4 = beep
    # 5 = Chime
    # 6 = Low Chime
    # 7 = High Chime

    lochime = 0x80 & chime
    repeats = repeats % 10

    bus = can.interface.Bus()
    msg = can.Message(arbitration_id=attarb,
                      data=[locchime, delay, repeats, 0xFF, 0x05 ],
                      extended_id=True)
    try:
        bus.send(msg)
        logging.info("Message sent on {}".format(bus.channel_info))
    except can.CanError:
        logginh.warning("Message NOT sent")
        return False

    return True
   
if __name__ == '__main__':
    sendchime(chime=5, repeat=2)
