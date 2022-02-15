"""
Starts the long-running HTTP client posting temperature and humidity
to a web server.

This program runs under MicroPython on the ESP-32.
"""
        
import post_dht22_data_to_database as post

post.main()
