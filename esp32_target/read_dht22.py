"""
Reads the DHT-22, and returns requested temp(s) and humidity as a dict.

This program runs under MicroPython on the ESP-32.
"""
from machine import Pin
from time import sleep
import dht


def read_dht22(c=True, f=True, h=True, upper=True):
    """
    Reads the DHT-22, and returns requested temp(s) and humidity as a dict.
    :param c: Boolean: return temp in C if True
    :param f: Boolean: return temp in F if True
    :param h: Boolean: return humidity if True
    :param upper: Boolean: Use uppercase dict keys if True
    :return: A dict with the selected information
    """
    sensor = dht.DHT22(Pin(14))
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()

        ret_dict = {}
        
        if c:
            key = 'C' if upper else 'c'
            ret_dict[key] = temp
        if f:
            key = 'F' if upper else 'f'
            ret_dict[key] = temp * (9/5) + 32.0
        if h:
            key = 'Humidity' if upper else 'h'
            ret_dict[key] = hum
        ret_dict['Error'] = False
        return ret_dict
    
    except OSError as e:
        return {"Error": True, "Message": f"Failed to read sensor: {e}"}
        
