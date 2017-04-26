# gmlan_gw

Currently this project is trying to learm more about GMLAN 29bit protocol.

Using a raspberry pi as the develompement platform along with a SWCAN pi plate. Logging is 
done with canutils candump. 

Logging: candump can0 -L > $logname
Playback: zcat log | canplayer vcan0=can0

running gmlan_gw.py while playing back a log will interpret IDs I am working on. 

More to come. Very early stages.

-- Setup for a raspberry pi:
/boot/config.txt
dtparam=spi=on
dtoverlay=mcp2515-can0,oscillator=16000000,interrupt=24

* Verify your interrupt pin and osc freq. I have both 8MHz and 16MHz MCP boards. Gotta match or you spend HOURS debugging. 

/etc/network/interfaces:

allow-hotplug can0
iface can0 can static
    bitrate 33000
    up /sbin/ip link set $IFACE down
    up /sbin/ip link set $IFACE up txqueuelen 1000 type can bitrate 33000 sample-point 0.7 triple-sampling off restart-m
s 500

auto vcan0
   iface vcan0 inet manual
   pre-up /sbin/ip link add dev $IFACE type vcan
   up /sbin/ifconfig $IFACE up

* vcan0 is used to play back logs to scripts under test/development.

-- Record of logs:
candump can0 -L > $logname

-- Playback of logs:
canplayer vcan0=can0 -I canlog.log
