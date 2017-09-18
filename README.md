#Gitlab RPI notifier


A small project that transforms your Raspberry PI zero + Unicorn pHAT into  build status monitor

----------

## How it works
The application runs a python web app that serve an admin panel where you can configure your Gitlab access and the position of the projects status on the unicorn leds.

The app also runs a cron job that pulls statuses from the latest gitlab pipeline builds and updates the leds accordingly.

## Installation and running
```
pip install -r requirements.txt
python run.py
```
Then go to http://{ip}:8080 to see the dashboard