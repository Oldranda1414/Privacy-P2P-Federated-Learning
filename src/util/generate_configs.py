import os
from sys import argv
# TODO implement this

def main():
    args = argv[1:]
    docker_compose_filepath = "src/docker/docker-compose.yml"
    peers_filepath = "src/main/peers.json"
    quiet = False
    if len(args) == 2:
        if args[1] == "-q":
            quiet = True
        else:
            print(f"-q is the only accepted flag")
    if not args:
        print(f"Usage: just run <number_of_peers>")
        return

    generate_docker_compose(docker_compose_filepath, number_of_peers)
    generate_peers_file(peers_filepath, number_of_peers)
    if not quiet:
        print(f"Config files generated to {os.path.abspath(docker_compose_filepath)} and {os.path.abspath(peers_filepath)}")

if __name__ == "__main__":
    main()
