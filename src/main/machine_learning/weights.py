import numpy as np

class Weights:
    def __init__(self, weights: list[np.ndarray]):
        self.weights: list[np.ndarray] = weights

    def as_flat_vector(self) -> np.ndarray:
        """Flatten all weights and biases into a single 1D vector."""
        return np.concatenate([w.flatten() for w in self.weights])

    def from_flat_vector(self, flat: np.ndarray) -> None:
        """Replace weights with values from a flat vector."""
        new_weights = []
        offset = 0
        for w in self.weights:
            size = np.prod(w.shape)
            new_w = flat[offset: offset + size].reshape(w.shape)
            new_weights.append(new_w)
            offset += size
        self.weights = new_weights

