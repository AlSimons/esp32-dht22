"""
A MicroPython web server which can return temperature and humidity readings.

This program runs under MicroPython on the ESP-32.
"""
import picoweb
import wifi_connect
from read_dht22 import read_dht22
import mytime
import ntptime

# Get online
ip_address = wifi_connect.connect()

# ntptime.settime sometimes times out.
success = False
while not success:
    try:
        ntptime.settime()
        success = True
    except OSError as e:
        print(e)

app = picoweb.WebApp("Weather") 


def format_time():
    t = mytime.get_local_time()
    return f"{t[0]}/{t[1]:02}/{t[2]:02} {t[3]:02}:{t[4]:02}:{t[5]:02}"


@app.route('/')
def index(req, resp):
    yield from picoweb.start_response(resp)
    
    yield from resp.awrite("""Hello world from picoweb running on the ESP32<br>&nbsp;<br>
                           To get the current weather data, add /wx to the URL you used.""")
    

@app.route('/wx')
def wx(req, resp):
    readings = read_dht22()

    yield from picoweb.start_response(resp)
    if readings["Error"]:
        yield from resp.awrite(f"WX reading failed: {readings['Message']}")
        return

    timeofday = format_time()
    page = \
        f"""<html>
        <head>
            <title>Al's weather</title>
            <meta http-equiv="refresh" content="30">
        </head>
        <body>
            The time is {timeofday}.<br>&nbsp;<br>
            Temp C: {readings['C']}<br>
            Temp F: {readings['F']}<br>
            Humidity: {readings['Humidity']}
        </body>
        </html>
        """    
    yield from resp.awrite(page)

# Now start the server...
app.run(debug=True, host = ip_address)
