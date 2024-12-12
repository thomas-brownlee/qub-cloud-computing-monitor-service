import html
import json
import threading
import time

import requests
from flask import Flask, Response
from flask_cors import CORS

from monitor.src.service_discovery import discovery

app = Flask(__name__)
CORS(app)

service_status = {}
service_list = {}

def service_down(service_name: str):
    pass

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
                statusUp = (response.status_code > 199 and response.status_code < 299)

            except requests.exceptions.RequestException:
                statusUp = False

            if not statusUp:
                service_down(service)
            
            service_status[address] = {
                "service_name":service,
                "last_check": time.time(),
                "status": statusUp
                }

    removed_services = {
        key: service_list["active_services"][key]
        for key in service_list["active_services"]
        if key not in latest_service_list["active_services"]
    }
    for service in removed_services:
        for service_addresses in removed_services[service].keys():
            service_status[service_addresses] = {
                    "service_name":service,
                    "last_check": time.time(),
                    "status": False
                    }
            
            service_down(service_addresses)

    service_list = latest_service_list


def test_services():
    global service_time_average
    global service_time_latest
    pass

def generate_html():
    global service_status
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
      <title>Service Status</title>
      <style>
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid black; padding: 8px; text-align: left; }
        .up { background-color: lightgreen; }
        .down { background-color: lightcoral; }
      </style>
      <meta http-equiv="refresh" content="5" />
    </head>
    <body>
        <h1>Service Status</h1>
        <table id="serviceTable">
            <thead>
                <tr>
                    <th>Service</th>
                    <th>URL</th>
                    <th>Last Checked</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
    """
    for url, service in service_status.items():
        status_text = "Up" if service['status'] else "Down"
        row_class = "up" if service['status'] else "down"
        html_content += f"""
        <tr class="{row_class}">
          <td>{html.escape(service['service_name'])}  
          <td>{html.escape(url)}</td>
          <td>{time.ctime(service['last_check'])}</td>
          <td>{status_text}</td>
        </tr>
        """
    html_content += """
            </tbody>
        </table>
    </body>
    </html>
    """
    return html_content


def update_status():
    global service_list
    service_list = discovery.get_active_services()

    while True:
        ping_services()
        time.sleep(5)


@app.route("/")
def get_status_html():
    return Response(
        generate_html(),
        mimetype="text/html",
    )


if __name__ == "__main__":
    thread = threading.Thread(target=update_status, daemon=True)
    thread.start()
    app.run(debug=True, use_reloader=False, threaded=True, host="0.0.0.0", port=80)
