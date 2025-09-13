import numpy as np
import json

from communication.encodable import Encodable

class Weights(Encodable):
    def __init__(self, weight_list: list[np.ndarray]):
        self._weights: list[np.ndarray] = weight_list

    def __str__(self):
        return str(self._weights)

    def as_list(self):
        return self._weights

    def as_flat_vector(self) -> np.ndarray:
        """Flatten all weights and biases into a single 1D vector."""
        return np.concatenate([w.flatten() for w in self._weights])

    def from_flat_vector(self, flat: np.ndarray) -> None:
        """Replace weights with values from a flat vector."""
        new_weights = []
        offset = 0
        for w in self._weights:
            size = np.prod(w.shape)
            new_w = flat[offset: offset + size].reshape(w.shape)
            new_weights.append(new_w)
            offset += size
        self._weights = new_weights

    @classmethod
    def to_dict(cls, obj: "Weights") -> dict:
        """Convert weights into a dict with lists for serialization."""
        return {
            "weights": [w.tolist() for w in obj._weights],
            "shapes": [w.shape for w in obj._weights],
            "dtypes": [str(w.dtype) for w in obj._weights],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Weights":
        weights = [
            np.array(arr, dtype=np.dtype(dt)).reshape(shape)
            for arr, shape, dt in zip(data["weights"], data["shapes"], data["dtypes"])
        ]
        obj = cls(weights)
        return obj

    @classmethod
    def encode(cls, obj: "Weights") -> bytes:
        """Encode to JSON string."""
        return (json.dumps(cls.to_dict(obj)) + "\n").encode()

    @classmethod
    def decode(cls, data: bytes) -> "Weights":
        """Decode JSON string to instance."""
        obj = json.loads(data.decode().strip())
        return cls.from_dict(obj)

