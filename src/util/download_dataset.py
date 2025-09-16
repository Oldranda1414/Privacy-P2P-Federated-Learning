import os
from sys import argv
import numpy as np
from tensorflow.keras.datasets import imdb

def vectorize_sequences(sequences, dimension=10000):
    results = np.zeros((len(sequences), dimension), dtype="float32")
    for i, sequence in enumerate(sequences):
        results[i, sequence] = 1.0
    return results

def save_imdb_dataset(filepath="imdb_dataset.npz", num_words=10000):
    """Download IMDB dataset, preprocess, and save to disk."""
    os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)

    (train_data, train_labels), (test_data, test_labels) = imdb.load_data(num_words=num_words)

    x_train = vectorize_sequences(train_data, dimension=num_words)
    x_test = vectorize_sequences(test_data, dimension=num_words)

    y_train = np.asarray(train_labels, dtype="float32")
    y_test = np.asarray(test_labels, dtype="float32")

    np.savez_compressed(filepath, 
                        x_train=x_train, y_train=y_train,
                        x_test=x_test, y_test=y_test)

def main():
    args = argv[1:]
    filepath = "dataset/imdb_dataset.npz"
    quiet = False
    if args:
        if args[0] == "-q":
            quiet = True
        else:
            raise ValueError("Invalid argument. Only '-q' is supported.")

    if os.path.exists(filepath) and not quiet:
        print(f"Dataset already exists at {os.path.abspath(filepath)} (skipping download)")
    else:
        save_imdb_dataset(filepath)
        if not quiet:
            print(f"Dataset downloaded to {os.path.abspath(filepath)}")

if __name__ == "__main__":
    main()
    
