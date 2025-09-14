import numpy as np
import os
from tensorflow.keras.datasets import imdb

from peers import get_peer_number, load_all_peers, Peer

# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress all TensorFlow logging
# os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'  # Additional suppression
SPLIT_SEED = 1

class Dataset:
    def __init__(self, train: tuple[np.ndarray, np.ndarray], test: tuple[np.ndarray, np.ndarray]):
        if train[0].shape[0] != train[1].shape[0]:
            raise ValueError(
                f"Number of train samples ({train[0].shape[0]}) != number of train labels ({train[1].shape[0]})"
            )
        if test[0].shape[0] != test[1].shape[0]:
            raise ValueError(
                f"Number of test samples ({test[0].shape[0]}) != number of test labels ({test[1].shape[0]})"
            )
        self.train = train
        self.test = test

    def as_tuples(self) -> tuple[tuple[np.ndarray, np.ndarray], tuple[np.ndarray, np.ndarray]]:
        return self.train, self.test

def get_validation_length() -> int:
    return int(10000/get_peer_number())

def get_dataset(owner: Peer) -> Dataset:
    peers = load_all_peers()
    ordered_peers = [value for _, value in sorted(peers.items())]
    owner_index = ordered_peers.index(owner)
    dataset = _load_IMDB()
    iid_datasets = _split_iid(dataset, len(ordered_peers), SPLIT_SEED)
    return iid_datasets[owner_index]

def _load_IMDB() -> Dataset:
    (train_data, train_labels), (test_data, test_labels) = imdb.load_data(num_words=10000)

    def vectorize_sequences(sequences, dimension=10000):
        results = np.zeros((len(sequences), dimension))
        for i, sequence in enumerate(sequences):
            for j in sequence:
                results[i, j] = 1
        return results
    x_train = vectorize_sequences(train_data)
    x_test = vectorize_sequences(test_data)

    y_train = np.asarray(train_labels).astype("float32")
    y_test = np.asarray(test_labels).astype("float32")
    return Dataset((x_train, y_train), (x_test, y_test))

def _split_iid(dataset: Dataset, num_peers: int, seed: int | None = None) -> list[Dataset]:
    """
    Split a Dataset into `num_peers` smaller IID Datasets with optional deterministic seed.

    Args:
        dataset: Original Dataset object.
        num_peers: Number of splits / peers.
        seed: Optional randomness seed

    Returns:
        List of Dataset objects, each with IID samples from the original.
    """
    train, test = dataset.as_tuples()
    
    if seed is not None:
        np.random.seed(seed)
    
    # Split training data
    n_train = train[0].shape[0]
    train_indices = np.random.permutation(n_train)
    train_splits = np.array_split(train_indices, num_peers)
    
    # Split test data
    n_test = test[0].shape[0]
    test_indices = np.random.permutation(n_test)
    test_splits = np.array_split(test_indices, num_peers)
    
    # Create datasets for each peer
    peer_datasets = []
    for i in range(num_peers):
        train_split = (train[0][train_splits[i]], train[1][train_splits[i]])
        test_split = (test[0][test_splits[i]], test[1][test_splits[i]])
        peer_datasets.append(Dataset(train_split, test_split))

    return peer_datasets
