from machine_learning.dataset import get_dataset
from machine_learning.dataset import _load_IMDB
from peers import load_all_peers
from machine_learning.model import Model
from machine_learning.dataset import get_dataset

def simple_dataset_loading():
    original = _load_IMDB()
    print("original loaded")
    nodes = load_all_peers()
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

def initialized_util():
    model = Model()
    try:
        model.get_weights()
    except RuntimeError as e:
        print(f"catched expected runtime error: {e}")
    model.initialize()
    print("initialized model")
    w = model.get_weights()
    print("no error thrown as expected")
    model = Model()
    model.set_weights(w)
    print(f"is model initialized after manually setting weights: {model.is_initialized()}")

def baseline_accuracy():
    model = Model()
    model.initialize()
    dataset = _load_IMDB
    for _ in range(15):
        history = model.train(dataset)
        print(f"validation accuracy: {history.validation_accuracy}")

def main():
    try:
        baseline_accuracy()
    except Exception as e:
        print(f"something went wrong: {e}")

if __name__ == "__main__":
    main()
    
