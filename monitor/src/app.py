import requests
import time
import threading
from flask import Flask, Response
from flask_cors import CORS
import html

app = Flask(__name__)
CORS(app)

service_status = {}
service_time_average = {}
service_time_latest = {}

def ping_services():
    global service_status
    pass

def test_services():
    global service_time_average
    global service_time_latest
    pass

def update_status():
    count = 0
    while True:
        count += 1
        if count <= 5:
            ping_services()
        if count <= 30:
            test_services()
        time.sleep(5)


@app.route('/')
def get_status_html():
    return Response(" <!DOCTYPE html><html><head><title>Service Status</title></head></html>", mimetype='text/html')


if __name__ == '__main__':
    thread = threading.Thread(target=update_status, daemon=True)
    thread.start()
    app.run(debug=True, use_reloader=False, threaded=True, port=3000)