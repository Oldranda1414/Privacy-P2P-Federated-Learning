import argparse
import time
from sys import argv

def run(role, target=None):
    if role == "ping":
        while True:
            print("PING ->", target, flush=True)
            time.sleep(2)
    elif role == "pong":
        while True:
            print("PONG <-", flush=True)
            time.sleep(2)
    else:
        raise ValueError("Unknown role")

if __name__ == "__main__":
    print("starting", flush=True)
    parser = argparse.ArgumentParser()
    parser.add_argument("--role", required=True, choices=["ping", "pong"])
    parser.add_argument("--target")
    args = parser.parse_args()
    run(args.role, args.target)
    print("ending", flush=True)

