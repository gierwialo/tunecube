#!/bin/bash

#check source: https://superuser.com/questions/1539634/pulseaudio-daemon-wont-start-inside-docker/1545361#1545361

pulseaudio -D --verbose --exit-idle-time=-1 --start

/usr/bin/chromium --window-size=800,600 --test-type --use-fake-ui-for-media-stream --ignore-certificate-errors https://tune_frontend

#xterm