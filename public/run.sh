#!/bin/bash

source ../env/bin/activate

cd scheduleServer
gunicorn scheduleServer.wsgi -b 127.0.0.1:$PORT -w=4