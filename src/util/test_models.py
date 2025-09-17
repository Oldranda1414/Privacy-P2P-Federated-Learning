import os
from sys import argv
import numpy as np
from tensorflow import keras
from tensorflow.keras import Model, layers
from tensorflow.keras.models import load_model
from tensorflow.keras.callbacks import EarlyStopping

def load_test_dataset(filepath: str) -> tuple[tuple[np.ndarray, np.ndarray], tuple[np.ndarray, np.ndarray]]:
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Dataset file {filepath} not found. Run 'just download_dataset' first.")
    
    with np.load(filepath) as data:
        x_train = data["x_train"]
        y_train = data["y_train"]
        x_test = data["x_test"]
        y_test = data["y_test"]

    return (x_train, y_train), (x_test, y_test)

def get_local_model(x_train: np.ndarray, y_train: np.ndarray) -> Model:
    model = keras.Sequential([
        keras.Input(shape=(10000,)),
        layers.Dense(16, activation="relu"),
        layers.Dense(16, activation="relu"),
        layers.Dense(1, activation="sigmoid")
        ])

    model.compile(optimizer="rmsprop", loss="binary_crossentropy", metrics=["accuracy"])

    validation_len = 10000
    x_val = x_train[:validation_len]
    partial_x_train = x_train[validation_len:]
    y_val = y_train[:validation_len]
    partial_y_train = y_train[validation_len:]
    early_stop = EarlyStopping(
        monitor='val_loss',
        patience=5,
        restore_best_weights=True
    )
    model.fit(
            partial_x_train,
            partial_y_train,
            epochs=50,
            batch_size=512,
            validation_data=(x_val, y_val),
            callbacks=[early_stop],
            verbose=0
        )
    return model

def main():
    args = argv[1:]
    if len(args) != 1:
        raise ValueError("usage: just test_model <number_of_peers>")

    try:
        number_of_peers = int(args[0])
    except ValueError:
        # TODO check if stuff works with 1 peer
        raise ValueError("<number_of_peers> must be an integer")
    dataset_path = "dataset/imdb_dataset.npz"
    peer_output_path = "docker/output/"
    peer_models: list[Model] = []
    peer_models_accuracies: list[float] = []

    (x_train, y_train), (x_test, y_test) = load_test_dataset(dataset_path)
    for i in range(1, number_of_peers + 1):
        peer_model_path = f"{peer_output_path}peer{i}/model.keras"
        peer_models.append(load_model(peer_model_path))
    local_model = get_local_model(x_train, y_train)

    original_accuracy = local_model.evaluate(x_test, y_test)[1]
    for model in peer_models:
        peer_models_accuracies.append(model.evaluate(x_test, y_test)[1])

    print(f"original accuracy: {original_accuracy}")
    for i, accuracy in enumerate(peer_models_accuracies):
        print(f"peer {i + 1} models accuracies: {accuracy}")

if __name__ == "__main__":
    main()
    
