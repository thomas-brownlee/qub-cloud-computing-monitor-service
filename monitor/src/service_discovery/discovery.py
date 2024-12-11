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

if __name__ == "__main__":
    containers = get_docker_containers_in_network()
