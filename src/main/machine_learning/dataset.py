import numpy as np
from typing import Tuple

class Dataset:
    def __init__(self, samples: np.ndarray, labels: np.ndarray):
        if samples.shape[0] != labels.shape[0]:
            raise ValueError(
                f"Number of samples ({samples.shape[0]}) != number of labels ({labels.shape[0]})"
            )
        self.samples = samples
        self.labels = labels

    def as_tuple(self) -> Tuple[np.ndarray, np.ndarray]:
        return self.samples, self.labels
