"""Calls on the docker compose api to get the information about other container in the image"""

import json
import subprocess

dictionary = {"active_services": {"service-name": {"host_address": "containers"}}}


def get_docker_containers_in_network():
    """Retrieves a list of Docker containers within a specific network using Docker CLI."""
    try:
        command = [
            "curl",
            "--unix-socket",
            "/var/run/docker.sock",
            "http://localhost/containers/json",
        ]
        result = subprocess.run(command, capture_output=True, text=True, check=True)

        containers = json.loads(result.stdout)

        return containers
    except subprocess.CalledProcessError as error:
        return False


def safe_get(d, keys, default=None):
    """Safely traverse a nested dictionary using a list of keys."""
    for key in keys:
        d = d.get(key, default)
        if d is default:
            return default
    return d


def generate_service_directorys(containers: dict):
    new_service_list = {}
    for container in containers:
        connected_network = "cluster_docker-network"
        container_id = container.get("Id")
        if not container_id:
            continue  # skip to next
        port = None
        for item in container.get("Ports", []):
            if item["Type"] == "tcp":
                port = item["PrivatePort"]
        if not port:
            print("No TCP port found, skipping container.")
            continue  # skip to the next items

        path = ["Labels", "com.docker.compose.service"]
        service_name = safe_get(container, path)
        if not service_name:
            continue  # skip to the next items
        print(f"Service Name: {service_name}")

        path = ["NetworkSettings", "Networks", connected_network, "IPAddress"]
        ip_address = safe_get(container, path)
        if not ip_address:
            continue  # skip to the next items
        print(f"IP Address: {ip_address}")

        # Create new entry as a dictionary with service name as key
        new_entry = {
            f"http://{ip_address}:{port}": container_id
        }

        # If "active_services" is not yet in new_service_list, create it
        if "active_services" not in new_service_list:
            new_service_list["active_services"] = {}

        # Update the active_services with the new entry
        new_service_list["active_services"].update({service_name: new_entry})

    return new_service_list

if __name__ == "__main__":
    containers = get_docker_containers_in_network()
    if containers:
        print(generate_service_directorys(containers))
