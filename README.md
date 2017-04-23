# gmlan_gw

Currently this project is trying to learm more about GMLAN 29bit protocol.

Using a raspberry pi as the develompement platform along with a SWCAN pi plate. Logging is 
done with canutils candump. 

Logging: candump can0 -L > $logname
Playback: zcat log | canplayer vcan0=can0

running gmlan_gw.py while playing back a log will interpret IDs I am working on. 

More to come. Very early stages.
