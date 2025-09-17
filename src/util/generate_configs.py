from sys import argv
from pathlib import Path
import yaml
import json

def generate_docker_compose(num_peers: int, output_file="docker-compose.generated.yml"):
    compose = {
        "services": {}
    }

    base_port = 8888
    for i in range(1, num_peers + 1):
        peer_name = f"peer{i}"
        service = {
            "ports": [f"{base_port + i - 1}:{base_port + i - 1}"],
            "environment": [f"NODE_ID=node{i}"],
            "build": {
                "context": "..",
                "dockerfile": "docker/Dockerfile"
            },
            "container_name": peer_name,
            "volumes": [f"./output/{peer_name}:/app/output"]
        }
        compose["services"][peer_name] = service

    with open(output_file, "w") as f:
        yaml.dump(compose, f, sort_keys=False)

def generate_peers_json(num_peers: int, output_file="peers.json"):
    peers_list = []
    base_port = 8888

    for i in range(1, num_peers + 1):
        peer = {
            "node_id": f"node{i}",
            "host": f"peer{i}",
            "port": base_port + i - 1
        }
        peers_list.append(peer)

    data = {"peers": peers_list}

    with open(output_file, "w") as f:
        json.dump(data, f, indent=2)

def main():
    args = argv[1:]
    if len(args) != 1:
        raise ValueError("usage: just test_model <number_of_peers>")

    try:
        number_of_peers = int(args[0])
    except ValueError:
        # TODO check if stuff works with 1 peer
        raise ValueError("<number_of_peers> must be an integer")
    docker_compose_path = "docker/docker-compose.generated.yml"
    peers_json_path = "src/main/peers.json"
    generate_docker_compose(number_of_peers, docker_compose_path)
    generate_peers_json(number_of_peers, peers_json_path)

if __name__ == "__main__":
    main()
    
