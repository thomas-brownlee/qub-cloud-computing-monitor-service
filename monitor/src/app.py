import requests
import time
import threading
from flask import Flask, Response
from flask_cors import CORS
import html

from monitor.src.service_discovery import discovery


app = Flask(__name__)
CORS(app)

service_status = {}
service_time_average = {}
service_time_latest = {}
service_list = {}


def ping_services():
    global service_status
    global service_list
    exclude_services = ["front-end", "monitor"]
    latest_service_list = discovery.get_active_services()

    for service in latest_service_list["active_services"]:
        if service in exclude_services:
            continue

        ip_addresses = latest_service_list["active_services"][service].keys()
        for address in ip_addresses:
            try:
                url = f"{address}/api/{service}/service/ping"
                response = requests.get(url, timeout=10)
                if response.status_code != 200:
                    pass  # Implements service down
                json_data = response.json()
                if json_data["status"] != "active":
                    pass  # Implement service down
            except requests.exceptions.RequestException:
                pass  # Implement service down
    removed_services = {
        key: service_list["active_services"][key]
        for key in service_list["active_services"]
        if key not in latest_service_list["active_services"]
    }
    for services in removed_services:
        pass  # Implement service down
    service_list = latest_service_list


def test_services():
    global service_time_average
    global service_time_latest
    pass


def update_status():
    global service_list
    service_list = discovery.get_active_services()
    count = 0
    while True:
        count += 1
        ping_services()
        if count <= 30:
            test_services()
            count = 0
        print(service_list)
        time.sleep(5)


@app.route("/")
def get_status_html():
    return Response(
        f" <!DOCTYPE html><html><head><title>Service Status</title></head><body>{service_list}</body></html>",
        mimetype="text/html",
    )


if __name__ == "__main__":
    # thread = threading.Thread(target=update_status, daemon=True)
    # thread.start()
    # app.run(debug=True, use_reloader=False, threaded=True, port=80)
    update_status()
