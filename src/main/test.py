from machine_learning.dataset import get_dataset
from machine_learning.dataset import _load_IMDB
from fsm.context import PEER_JSON_FILE
from peers import load_all_peers

try:
    original = _load_IMDB()
    print("original loaded")
    nodes = load_all_peers(PEER_JSON_FILE)
    print("nodes loaded")
    datasets = []
    get_dataset(list(nodes.values())[0])
    print("after first get")
    get_dataset(list(nodes.values())[1])
    print("after second get")
    for node in nodes.values():
        datasets.append(get_dataset(node))
    original_len = len(original.train[0])
    split_len = 0
    for dataset in datasets:
        split_len += len(dataset.train[0])
    print(f"original len = {original_len}")
    print(f"split len = {split_len}")
except Exception as e:
    print(f"something went wrong: {e}")
