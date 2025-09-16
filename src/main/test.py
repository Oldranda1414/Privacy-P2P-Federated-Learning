from numpy import array, zeros

from machine_learning.dataset import get_dataset
from machine_learning.dataset import _load_IMDB
from peers import load_all_peers
from machine_learning.model import Model
from machine_learning.dataset import get_dataset
from machine_learning.weights import Weights, sum_weights
from sac import generate_partitions

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
    dataset = _load_IMDB()
    for _ in range(15):
        history = model.train(dataset)
        print(f"validation accuracy: {history.validation_accuracy}")

def weight_partition():
    arr = array([[1.1, 2.2],
                [3.3, 4.4]])
    weights = Weights([arr])
    partitions = generate_partitions(weights, 2)
    reconstructed = sum_weights(partitions)
    print(f"original weights: {weights}")
    print(f"reconstructed weights: {reconstructed}")

def secure_avarage_computation():
    arr1 = array([[1.1, 2.2],
                [3.3, 4.4]])
    arr2 = array([[2.1, 1.2],
                [4.3, 3.4]])
    arr3 = array([[4.1, 3.2],
                [1.3, 5.4]])
    weights1 = Weights([arr1])
    weights2 = Weights([arr2])
    weights3 = Weights([arr3])
    expected_average = sum_weights([weights1, weights2, weights3]) / 2
    print(f"expected average: {expected_average}")
    # partitioning
    partitions1 = generate_partitions(weights1, 3)
    partitions2 = generate_partitions(weights2, 3)
    partitions3 = generate_partitions(weights3, 3)
    # subtotal
    subtotal1 = partitions1[0] + partitions2[1] + partitions3[2]
    subtotal2 = partitions1[2] + partitions2[0] + partitions3[1]
    subtotal3 = partitions1[1] + partitions2[2] + partitions3[0]
    # total
    computed_total = sum_weights([subtotal1, subtotal2, subtotal3]) / 3
    print(f"computed: {computed_total}")

def main():
    try:
        secure_avarage_computation()
    except Exception as e:
        print(f"something went wrong: {e}")

if __name__ == "__main__":
    main()
    
