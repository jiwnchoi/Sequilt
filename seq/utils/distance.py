import numpy as np
from numba import jit


def get_distance(x: np.ndarray) -> np.ndarray:
  seq1 = x[:, np.newaxis, :]
  seq2 = x[np.newaxis, :, :]
  distances = seq1 != seq2
  zero_distances = np.logical_and(seq1 == 0, seq2 == 0)
  distances = np.maximum(distances, zero_distances)

  distances = np.sum(distances, axis=2) / x.shape[1]
  np.fill_diagonal(distances, 0)

  return distances


@jit(nopython=True, parallel=True)
def get_distance_numba(x: np.ndarray) -> np.ndarray:
  n = x.shape[0]
  m = x.shape[1]
  distances = np.zeros((n, n), dtype=np.float64)

  for i in range(n):
    for j in range(i + 1, n):
      dist = 0
      for k in range(m):
        if x[i, k] != x[j, k] or (x[i, k] == 0 and x[j, k] == 0):
          dist += 1
      distances[i, j] = distances[j, i] = dist / m

  return distances


__all__ = ["get_distance"]