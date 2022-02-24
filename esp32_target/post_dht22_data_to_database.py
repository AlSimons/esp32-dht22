"""
Uses HTTP POST to send DHT22 data to a database web server.
Has a URL for the web server hardcoded, which will need to be changed.

This program runs under MicroPython on the ESP-32.
"""
import json
import urequests
import wifi_connect
from read_dht22 import read_dht22
import machine
import mytime
import ntptime
from time import sleep

# THIS URL NEEDS TO BE CHANGED TO YOUR NETWORK ENVIRONMENT!
database_server_url = 'http://192.168.0.238:8080/post_weather_data'


def set_rtc():
    # ntptime.settime() sometimes times out.
    success = False
    while not success:
        try:
            ntptime.settime()
            success = True
            print("Set clock OK!")
        except OSError as e:
            print(e)


def format_time():
    # Returns an ISO-formatted date time string.  Compatible with sqlite3
    t = mytime.get_local_time()
    return f"{t[0]}-{t[1]:02}-{t[2]:02} {t[3]:02}:{t[4]:02}:{t[5]:02}"


def main():
    ip_address = wifi_connect.connect()
    print("**", ip_address)
    set_rtc()

    # This does not need to be in a loop, because waking from deepsleep() restarts
    # the program from scratch

    data = read_dht22(c=False, upper=False)

    data['date_time'] = format_time()
    json_data = json.dumps(data)

    response = urequests.post(database_server_url, data=json_data)

    print("""
Sleeping for 30 seconds to allow you load a different program (e.g., a different main.py).
After that we will be in deep sleep for 150 seconds (total cycle time 3 min). During
deep sleep you will not be able to access the system.""")
    sleep(30)  # 30 seconds
    print("Going to deep sleep now")
    
    machine.deepsleep(150 * 1000)  # deepsleep() takes milliseconds
    print("This will never be printed.")
