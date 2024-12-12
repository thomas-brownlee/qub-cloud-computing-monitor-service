"""Holds the starting point for the monitoring service"""

import time

import requests

from monitor.src.service_discovery import discovery


def ping_services():
    """Runs a loop  that pings the services"""
    existing_service_list = discovery.get_active_services()
    exclude_services = ["front-end", "char-count", "word-count", "monitor"]
    while True:
        time.sleep(15)
        print("Pinging Services in list")
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
                        pass #Implements service down
                    json_data = response.json()
                    if json_data["status"] != "active":
                        pass #Implement service down
                except requests.exceptions.RequestException:
                    pass #Implement service down

        removed_services = {key: existing_service_list['active_services'][key] for key in existing_service_list['active_services'] if key not in latest_service_list['active_services']}
        for services in removed_services:
            pass #Implement service down        
        existing_service_list = latest_service_list



if __name__ == "__main__":
    ping_services()
