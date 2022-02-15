# esp32-dht22
This is a play program which I used to start learning about MicroPython on the
ESP32 development boards.

I flashed MicroPython onto one of my ESP32s and wired it to a DHT22 sensor. 
There are many tutorials and references on the web for both of those steps, 
so I won't go into them here.

This repo contains files destined for the ESP32 in directory esp32_target.
In the top level directory are files intended for
a computer with real (Macro?) Python.

## The esp32-target directory
All of these files are intended to be loaded onto your ESP32.  I use the ampy 
program running on my Pi to do that.

There are actually two main programs in here.
### web_server.py
This is not the current program.  This makes the ESP32 into a webserver which
serves the DHT22 data on the /wx endpoint. 

To run this program, change the main.py program to be
```python
import weather_server
```
  
### post_dht22_data_to_database.py:
This is the current program. It uses html POST requests to send data to the 
web server contained in weather_server.py, in the main directory of this 
repo.  It is currently configured to return Fahrenheit; to use Celsius
change the line:
```python
data = read_dht22(c=False, upper=False)

# to

data = read_dht22(c=True, upper=False)
```

### Other files
The other files in the esp32_target directory are helper modules used by
both of the above programs.
* mytime.py
* read_dht22.py
* wifi_connect.py
  * Requires a file wifi_credentials.py which is not included in this repo.
  It contains a single line
```python
creds = {'SSID': 'your ssid', 'PASS': 'your wifi password'}
```
* and of course, main.py, which is invoked by the MicroPython infrastructure.

## The top-level directory
These programs do not run on the ESP32, but on a system with "real" Python.

### weather_server.py
I run this on my Raspberry Pi 4B. It is the web server which is used by
post_dht22_data_to_database.  It creates and maintains a sqlite3 database
DHT_data.db for the DHT22 data in the current directory.

### plot_esp32_dht22_data.py
This program plots the data contained in the sqlite3 database.
It has three command line options:
* --start-date: Date of earliest desired data. Must be in the format 
YYYY-MM-DD. Default: earliest available date.
* --end-date: Date of last desired data. Must be in the format YYYY-MM-DD.
Default: latest available date.
* --num-points: Number of points to plot. Default=1000. With large databases
this can greatly speed up drawing the plots by only using a subset of the 
data.

NOTE: I have not yet gotten this to run on the Raspberry Pi. Installing 
matplotlib requires libcblas.so, for which I have not yet found a repository
from which to apt install it.  It is my intent to eventually make this run on 
the Pi too.