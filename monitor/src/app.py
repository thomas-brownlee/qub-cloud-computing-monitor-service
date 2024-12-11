"""Holds the starting point for the monitoring service"""

from monitor.src.service_discovery import discovery
from monitor.src.email_service import service_down_email
import requests
import time

ping_list_of_services = discovery.get_active_services()



def ping_services():
    exclude_services = ["front-end","char-count", "word-count", "monitor"]
    while True:
        time.sleep(3)
        ping_list_of_services = discovery.get_active_services()

        for service in ping_list_of_services['active_services']:
            if service in exclude_services:
                continue
            ip_addresses = ping_list_of_services['active_services'][service].keys()
            for address in ip_addresses:
                url = f"{address}/api/{service}/service/ping"
                response = requests.get(url, timeout=10)
                if response.status_code != 200:
                    service_down_email.send_service_down(service)
                json_data = response.json()
                if (json_data["status"] != "active"):
                    service_down_email.send_service_down(service)

    
        


if __name__ == "__main__":
    ping_services()
