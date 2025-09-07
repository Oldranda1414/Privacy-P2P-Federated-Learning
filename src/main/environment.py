import os

def get_self_id() -> str:
    return os.getenv('NODE_ID', 'default_node')
