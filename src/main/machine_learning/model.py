from tensorflow import keras
from tensorflow.keras import layers

from machine_learning.weights import Weights

class Model:
    def __init__(self):
        self.keras_model = keras.Sequential([
            keras.Input(shape=(10000,)),
            layers.Dense(16, activation="relu"),
            layers.Dense(16, activation="relu"),
            layers.Dense(1, activation="sigmoid")
            ])
        self.keras_model.compile(optimizer="rmsprop", loss="binary_crossentropy", metrics=["accuracy"])

    def get_weights(self):
        return Weights(self.keras_model.get_weights())

    def set_weights(self, new_weights: Weights):
        self.keras_model.set_weights(new_weights.as_list())

