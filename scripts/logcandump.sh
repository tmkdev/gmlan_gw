#!/bin/bash

logdir=/canlogs

mkdir -p $logdir

find $logdir/ -size 0 -delete
gzip $logdir/*.log

logname=$logdir/rawlog_$(date +'%Y%m%d%H%M').log
candump can0 -L > $logname
