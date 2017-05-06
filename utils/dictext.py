#!/usr/bin/python
from __future__ import print_function
import logging
import can
import re
import time

pimcu=0x099
attarb = ( 0x4 << 26) | (0x0185 << 13) | pimcu
txtarb = ( 0x4 << 26) | (0x0186 << 13) | pimcu
maxpacketlen = 3

def slicetext(text):
    trunc = (maxpacketlen * 6) - 1
    text=text[:trunc]

    text+= chr(0x04)
    parts = re.findall(".{1,6}", text)
    
    return parts[:maxpacketlen]

def sendtext(text):
    #0185 0097 000262020019
    #0186 0097 2702426C7565746F
    #0186 0097 26026F7468040000

    textparts = slicetext(text)
    messages = []
    bus = can.interface.Bus()

    messages.append(can.Message(arbitration_id=attarb,
                      data=[0x00, 0x02, 0x62, 0x02, 0x00, 0x19],
                      extended_id=True))

    for index, part in enumerate(textparts):
        if index == 0:
            data = [0x27, len(textparts)]
        else:
            data=[0x26, index+1 ]

        data += list(bytearray(part)) + [ 0,0,0,0,0,0 ]
        data = data[:8]

        messages.append(can.Message(arbitration_id=txtarb,
            data=data,
            extended_id=True))

    for message in messages:
        try:
            bus.send(message)
            logging.info("Message sent on {}".format(bus.channel_info))
            time.sleep(0.05)
        except can.CanError:
            logging.warning("Message NOT sent")
            return False

    return True

def cleartext():
    #0185 0097 00 02 60 02 00 19
    bus = can.interface.Bus()
    msg = can.Message(arbitration_id=attarb,
                      data=[0x00, 0x02, 0x60, 0x02, 0x00, 0x19],
                      extended_id=True)
    try:
        bus.send(msg)
        logging.info("Message sent on {}".format(bus.channel_info))
    except can.CanError:
        logginh.warning("Message NOT sent")
        return False

    return True
   
if __name__ == '__main__':
    print(sendtext('BobbiC'))
    print(sendtext('Bobbi Cahill'))
    print(sendtext('Bobbi Cahill loves Terry!'))
    print(cleartext())
