"""
Optimized similarity calculations for the recommendation system.
"""
import numpy as np
cimport numpy as np
from libc.math cimport sqrt

# Use 64-bit floats for better precision
DTYPE = np.float64
ctypedef np.float64_t DTYPE_t

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef np.ndarray[DTYPE_t, ndim=2] calculate_similarities(
    np.ndarray[DTYPE_t, ndim=2] item_user_matrix
):
    """
    Calculate item-item similarity matrix using Cython.
    """
    cdef:
        Py_ssize_t n_items = item_user_matrix.shape[0]
        Py_ssize_t n_users = item_user_matrix.shape[1]
        Py_ssize_t i, j, k
        DTYPE_t dot, norm_i, norm_j, sim
        np.ndarray[DTYPE_t, ndim=2] similarities = np.zeros((n_items, n_items), dtype=DTYPE)
    
    # Calculate similarities
    for i in range(n_items):
        for j in range(i, n_items):
            # Calculate dot product and norms
            dot = 0.0
            norm_i = 0.0
            norm_j = 0.0
            
            for k in range(n_users):
                dot += item_user_matrix[i, k] * item_user_matrix[j, k]
                norm_i += item_user_matrix[i, k] * item_user_matrix[i, k]
                norm_j += item_user_matrix[j, k] * item_user_matrix[j, k]
            
            # Calculate cosine similarity
            if norm_i > 0 and norm_j > 0:
                sim = dot / (sqrt(norm_i) * sqrt(norm_j))
            else:
                sim = 0.0
            
            similarities[i, j] = sim
            if i != j:  # Mirror to lower triangle
                similarities[j, i] = sim
    
    return similarities
