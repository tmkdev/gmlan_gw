#!/usr/bin/python
from __future__ import print_function
import logging
import can
import re
import time

#Personal Communications between 0x90 and 0x97
pimcu=0x092
attarb = ( 0x4 << 26) | (0x0185 << 13) | pimcu
txtarb = ( 0x4 << 26) | (0x0186 << 13) | pimcu

headers = {
    'directions': [0x00, 0x02, 0x36, 0x04, 0x80, 0x00],
    'display': [0x00, 0x02, 0x62, 0x02, 0x00, 0x19],
    'clear': [0x00, 0x02, 0x60, 0x02, 0x00, 0x19],
}

directiondict = {
    'name': 'IKEA SAN DIEGO',
    'streetnumber': '2149',
    'streetname': 'FENTON',
    'streettype': 'PKWY', 
    'city': 'SAN DIEGO', 
    'state': 'CA',
    'longitude': -117.126403,
    'latitude': 32.78004,
    'phone': '18888884532'
}

def slicetext(text, maxpacketlen=5):
    trunc = (maxpacketlen * 6) - 1
    text=text[:trunc]

    text+= chr(0x04)
    parts = re.findall(".{1,6}", text)
    
    return parts[:maxpacketlen]

def slicetext(text):
    slices = []
    for i in range(0, len(text), 6):
        slices.append(text[i:i + 6])

    return slices
    
def attribute_header(headertype):
    msg = can.Message(arbitration_id=attarb,
                      data=headers[headertype],
                      extended_id=True)

    sendmessages([msg])

def senddirections(directions):
    string="\x01{name}\n\x02{streetnumber}\n\x04{streetname}\n\x05{streettype}\n\x07{city}\n\x08{state}\n\x09{longitude:+.4f}\n\x0b{latitude:+.4f}\n\x0c{phone}\n".format(**directions) 
    textparts = slicetext(string)

    attribute_header('directions')
    messages = []

    for index, part in enumerate(textparts):
        if index == 0:
            data = [0x23, len(textparts)]
        else:
            data=[0x22, index+1 ]

        data += list(bytearray(part)) + [ 0,0,0,0,0,0 ]
        data = data[:8]

        messages.append(can.Message(arbitration_id=txtarb,
            data=data,
            extended_id=True))

    return sendmessages(messages)

def sendtext(text):
    #0185 0097 000262020019
    #0186 0097 2702426C7565746F
    #0186 0097 26026F7468040000
    maxlength = 29 # 5 packets * 6 bytes + end char (0x04)

    text = text[:maxlength] + chr(0x04)
    textparts = slicetext(text)
    messages = []
    attribute_header('display')

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

    return sendmessages(messages)

def cleartext():
    attribute_header('clear')

def sendmessages(messages):
    bus = can.interface.Bus()

    for message in messages:
        try:
            bus.send(message)
            logging.info("Message sent on {}".format(bus.channel_info))
            time.sleep(0.01)
        except can.CanError:
            logging.warning("Message NOT sent")
            return False

    return True
   
if __name__ == '__main__':
    print(senddirections(directiondict))
    #print(sendtext('Test'))
    #time.sleep(1)
    #print(sendtext('Test Test!'))
    #time.sleep(1)
    #print(sendtext('Test Test Test Test Test Test'))
    #time.sleep(2)
