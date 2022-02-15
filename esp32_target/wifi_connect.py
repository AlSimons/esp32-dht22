"""
Connects an ESP32 to a wifi access point.

This program runs under MicroPython on the ESP-32.
"""
import network

#
# wifi_credentials is not included in this repository. It contains the
# following line of code:
# creds = {'SSID': 'your ssid', 'PASS': 'your wifi password'}
#
from wifi_credentials import creds


def connect():
    """
    Connects to the wifi SSID specific in the wifi_credentials file.
    :return: The ESP32's  IP address.
    """
    ssid = creds['SSID']
    password = creds['PASS']

    station = network.WLAN(network.STA_IF)

    if station.isconnected():
        print("Already connected")
        return station.ifconfig()[0]

    station.active(True)
    station.connect(ssid, password)

    while not station.isconnected():
        pass

    print("Connection successful")

    config = station.ifconfig()
    print(config)

    # Return our IP address
    return config[0]
