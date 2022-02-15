#! /usr/bin/env python
"""
A web server which accepts POSTs of DHT-22 data from
post_dht22_data_to_database.py and saves in an sqlite3 database.

This program runs on, e.g., a Raspberry Pi, NOT the ESP32.
"""
from flask import Flask, redirect, url_for, request
import json
import sqlite3
import sys


def load_database(entry_as_json_string):
    entry = json.loads(entry_as_json_string)

    try:
        conn = sqlite3.connect("DHT_data.db")
        conn.execute("""CREATE TABLE IF NOT EXISTS readings(
            date_time TEXT,
            temp FLOAT,
            humidity FLOAT)""")
    except sqlite3.OperationalError as e:
        print("CONNECT FAILED", e, file=sys.stderr)
        return
    
    try:
        conn.execute(f"""
            INSERT INTO readings
                (date_time, temp, humidity)
            VALUES
                ("{entry['date_time']}", 
                 {entry['f']}, 
                 {entry['h']})
        """)
    except Exception as e:
        print("Insertion failed", e)
    
    try:
        conn.commit()
    except Exception as e:
        print("Commit failed", e)
        

app = Flask(__name__)


@app.route('/')
def tester():
    return "Got here"


@app.route('/post_weather_data', methods=['POST'])
def record_it():
    if request.method != 'POST':
        # can this happen?
        print('Received a request that was not a POST')
        return
    load_database(request.data)
    return 'success'


if __name__ == "__main__":
    app.run(host='192.168.0.238', port=8080)
