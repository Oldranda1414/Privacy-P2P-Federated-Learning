from tensorflow import keras
from tensorflow.keras import layers

from machine_learning.weights import Weights
from machine_learning.dataset import Dataset, get_validation_length
from utils.required_init import requires_initialization

class Model:
    def __init__(self):
        self.keras_model = keras.Sequential([
            keras.Input(shape=(10000,)),
            layers.Dense(16, activation="relu"),
            layers.Dense(16, activation="relu"),
            layers.Dense(1, activation="sigmoid")
            ])
        self.keras_model.compile(optimizer="rmsprop", loss="binary_crossentropy", metrics=["accuracy"])
        self._initialized = False

    def initialize(self):
        self._initialized = True

    def is_initialized(self) -> bool:
        return self._initialized

    @requires_initialization
    def get_weights(self):
        return Weights(self.keras_model.get_weights())

    def set_weights(self, new_weights: Weights):
        self.keras_model.set_weights(new_weights.as_list())
        self.initialize()

    @requires_initialization
    def train(self, dataset: Dataset):
        x_train, y_train = dataset.train
        validation_len = get_validation_length()
        x_val = x_train[:validation_len]
        partial_x_train = x_train[validation_len:]
        y_val = y_train[:validation_len]
        partial_y_train = y_train[validation_len:]
        self.keras_model.fit(
                partial_x_train,
                partial_y_train,
                epochs=1,
                batch_size=512,
                validation_data=(x_val, y_val)
            )
        return Weights(self.keras_model.get_weights())
