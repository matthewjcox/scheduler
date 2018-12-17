#!/bin/bash

source ../env/bin/activate

cd scheduleServer
echo "\n\n\n starting new server run \n"
gunicorn scheduleServer.wsgi -b 127.0.0.1:$PORT -w=4