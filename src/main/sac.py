from random import Random
from numpy import ndarray, zeros_like

from machine_learning.weights import Weights

RANDOM_MIN = 1
RANDOM_MAX = 100

def generate_partitions(weights: Weights, number_of_partitions: int, seed: int = 1) -> list[Weights]:
    rng = Random(seed)
    new_weights_list: list[list[ndarray]] = [[] for _ in range(number_of_partitions)]

    for tensor in weights.as_list():
        new_tensor_list = _generate_new_tensor_list(tensor, number_of_partitions, rng)
        for new_weights, new_tensor in zip(new_weights_list, new_tensor_list):
            new_weights.append(new_tensor)

    return [Weights(new_weights) for new_weights in new_weights_list]

def _generate_new_tensor_list(original_tensor: ndarray, number_of_partitions: int, rng: Random) -> list[ndarray]:
    new_tensor_list = [zeros_like(original_tensor) for _ in range(number_of_partitions)]
    if original_tensor.ndim == 2:
        # regular 2D weight matrix
        for i in range(original_tensor.shape[0]):
            for j in range(original_tensor.shape[1]):
                norm_partitions = _generate_normalized_partitions(original_tensor[i, j], number_of_partitions, rng)
                for k in range(number_of_partitions):
                    new_tensor_list[k][i, j] = norm_partitions[k]
    elif original_tensor.ndim == 1:
        # biases or 1D arrays
        for i in range(original_tensor.shape[0]):
            norm_partitions = _generate_normalized_partitions(original_tensor[i], number_of_partitions, rng)
            for k in range(number_of_partitions):
                new_tensor_list[k][i] = norm_partitions[k]
    elif original_tensor.ndim == 0:
        # scalar weight
        norm_partitions = _generate_normalized_partitions(original_tensor.item(), number_of_partitions, rng)
        for k in range(number_of_partitions):
            new_tensor_list[k][()] = norm_partitions[k]
    else:
        raise ValueError(f"Unsupported weight array with ndim={original_tensor.ndim}")
    return new_tensor_list

def _generate_normalized_partitions(weight: float, number_of_partitions: int, rng: Random) -> list[float]:
    partitions = [int(rng.uniform(RANDOM_MIN, RANDOM_MAX)) for _ in range(number_of_partitions)]
    partition_sum = sum(partitions)

    normalized_partitions = [weight * p / partition_sum for p in partitions]

    # Fix rounding error
    diff = weight - sum(normalized_partitions)
    normalized_partitions[0] += diff

    return normalized_partitions

