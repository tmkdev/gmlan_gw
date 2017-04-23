#!/usr/bin/python
from __future__ import print_function
import time
import os
import logging
import can
import struct
from collections import Counter

import polyline

logging.basicConfig(level=logging.INFO)

#        self.timestamp = timestamp
#        self.id_type = extended_id
#        self.is_extended_id = extended_id
#        self.is_remote_frame = is_remote_frame
#        self.is_error_frame = is_error_frame
#        self.arbitration_id = arbitration_id

class GMLAN(can.Listener):
    def __init__(self):
        self.handlers = {
            0x001: self._power,
            0x186: self._text,
            0x185: self._textparam,
            0x061: self._exttemp,
            0x005: self._tpms,
            #0x18e: self._textparam,
            0x026: self._fuel,
            0x053: self._gpsdate,
            0x055: self._gps,
        }

        self.counter = Counter() 
        self.locations = []
        self.fuel = [0,0]

    def _power(self, msg):
        status = { 0x0a: 'Ignition',
                   0x00: 'Power Off',
                   0x09: 'Accessory',
                }
        try:
            pstat=status[msg.data[0]]
            self.counter[pstat] += 1

            print(pstat)

            if self.counter[status[0x0a]] > 1 and self.counter[status[0x00]] > 2:
                print('Power Down Pi!')

        except:
            pass
    
    def _gps(self, msg):
        lat = (msg.data[0] << 24) | (msg.data[1] << 16) | (msg.data[2] << 8 )| msg.data[3]
        lon = (msg.data[4] << 24) | (msg.data[5] << 16) | (msg.data[6] << 8 )| msg.data[7]

        latvalid = (0x40000000 & lat) >> 30
        lonvalid = (0x40000000 & lon) >> 31

        latitude = (lat / 3600000.0)
        longitude = (lon / 3600000.0) -596.52325

        print(latitude, longitude)

        if not (latvalid & lonvalid):
            self.locations.append((latitude, longitude))

    def _gpsdate(self, msg):
        year = msg.data[0] + 2000
        month = msg.data[1]
        day = msg.data[2]
        hour = ( msg.data[3] >> 1 )
        minute = ( msg.data[4] >> 1 )
        second = ( msg.data[5] >> 1 )
        print('{}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}'.format(year, month, day, hour, minute, second))


    def _fuel(self, msg):
        fuel = msg.data[1]/2.56
        if self.fuel[0] == 0:
            self.fuel[0] = fuel
        self.fuel[1] = fuel

    def _text(self, msg):
        text = msg.data[2:].decode('utf-8')
        print(text)

    def _textparam(self, msg):
        print(msg)
        print(polyline.encode(self.locations, 5))

    def _exttemp(self, msg):
        temp = ( msg.data[1] / 2 ) - 40
        print("Ext Temp: {}C".format(temp))

    def _tpms(self, msg):
        p1 = msg.data[2] / 2
        p2 = msg.data[3] / 2
        p3 = msg.data[4] / 2
        p4 = msg.data[5] / 2

        print("TPMS: {} {} {} {}".format(p1, p2, p3, p4))

    def parse_gmlan(self,msg):
        if msg.is_extended_id:
            priority = msg.arbitration_id >> 26
            arb_id = ( msg.arbitration_id & (0x1FFF << 13) ) >> 13
            address = ( msg.arbitration_id & 0x1FFF )
        else:
            priority = msg.arbitration_id >> 12 
            arb_id = ( msg.arbitration_id & (0xf << 8) ) >> 8
            address = ( msg.arbitration_id & 0xFF )

        return priority, arb_id, address


    def on_message_received(self, msg):
        canid = msg.arbitration_id
        data = msg.data
        priority, arb_id, address = self.parse_gmlan(msg)

        msg.priority = priority
        msg.gm_arb_id = arb_id
        msg.gm_address = address

        if arb_id in self.handlers:
            self.handlers[arb_id](msg)
   
    def stop(self):
        pass

if __name__ == "__main__":
    bus = can.interface.Bus()
    notifier = can.Notifier(bus, [GMLAN(), can.CSVWriter('can.csv')])

    while True:
        time.sleep(.5)
