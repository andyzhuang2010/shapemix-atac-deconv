"""Small synthetic demonstration with known reference signatures."""
import numpy as np
from shapemix_atac import ShapeMixConfig, fit_shapemix_map

A = np.full((2, 6), 10.0)
omega = np.empty((2, 6, 3))
omega[0] = (0.8, 0.1, 0.1)
omega[1] = (0.1, 0.1, 0.8)
abundance = np.array([[8., 2.], [2., 8.], [6., 4.]])
counts = np.rint(np.einsum("sc,cp,cpb->spb", abundance, A, omega)).astype(int)
result = fit_shapemix_map(
    counts, A, omega, 100.0,
    config=ShapeMixConfig(max_steps=1000, patience=25),
    outer_split_seed=0, inner_mixture_seed=0,
)
print("Estimated proportions:")
print(result.proportions)
print("Expected proportions:")
print(abundance / abundance.sum(axis=1, keepdims=True))
