""
Cython-optimized similarity calculations for the recommendation system.
"""
import numpy as np
cimport numpy as np
from libc.math cimport sqrt
from cython import boundscheck, wraparound

# Use 64-bit floats for better precision
DTYPE = np.float64
ctypedef np.float64_t DTYPE_t

@boundscheck(False)
@wraparound(False)
cpdef double cosine_similarity(
    np.ndarray[DTYPE_t, ndim=1] u,
    np.ndarray[DTYPE_t, ndim=1] v
) except -1:
    """
    Calculate cosine similarity between two vectors using Cython for speed.
    
    Args:
        u: First vector
        v: Second vector
        
    Returns:
        double: Cosine similarity between u and v
    """
    cdef:
        Py_ssize_t i, n = u.shape[0]
        DTYPE_t dot_product = 0.0
        DTYPE_t norm_u = 0.0
        DTYPE_t norm_v = 0.0
        DTYPE_t ui, vi
    
    # Calculate dot product and norms in a single loop
    for i in range(n):
        ui = u[i]
        vi = v[i]
        dot_product += ui * vi
        norm_u += ui * ui
        norm_v += vi * vi
    
    # Avoid division by zero
    if norm_u == 0.0 or norm_v == 0.0:
        return 0.0
    
    return dot_product / (sqrt(norm_u) * sqrt(norm_v))

@boundscheck(False)
@wraparound(False)
cpdef np.ndarray[DTYPE_t, ndim=2] calculate_user_similarities(
    np.ndarray[DTYPE_t, ndim=2] user_item_matrix
):
    """
    Calculate user-user similarity matrix using Cython.
    
    Args:
        user_item_matrix: User-item interaction matrix
        
    Returns:
        np.ndarray: User similarity matrix
    """
    cdef:
        Py_ssize_t n_users = user_item_matrix.shape[0]
        Py_ssize_t i, j
        np.ndarray[DTYPE_t, ndim=2] similarities = np.zeros((n_users, n_users), dtype=DTYPE)
    
    # Calculate similarities for upper triangle and mirror to lower triangle
    for i in range(n_users):
        for j in range(i, n_users):
            sim = cosine_similarity(user_item_matrix[i], user_item_matrix[j])
            similarities[i, j] = sim
            if i != j:  # Avoid setting diagonal twice
                similarities[j, i] = sim
    
    return similarities

@boundscheck(False)
@wraparound(False)
cpdef np.ndarray[DTYPE_t, ndim=2] calculate_item_similarities(
    np.ndarray[DTYPE_t, ndim=2] user_item_matrix
):
    """
    Calculate item-item similarity matrix using Cython.
    
    Args:
        user_item_matrix: User-item interaction matrix (transposed for item similarities)
        
    Returns:
        np.ndarray: Item similarity matrix
    """
    # Transpose the matrix to get items as rows
    cdef np.ndarray[DTYPE_t, ndim=2] item_user_matrix = user_item_matrix.T
    cdef:
        Py_ssize_t n_items = item_user_matrix.shape[0]
        Py_ssize_t i, j
        np.ndarray[DTYPE_t, ndim=2] similarities = np.zeros((n_items, n_items), dtype=DTYPE)
    
    # Calculate similarities for upper triangle and mirror to lower triangle
    for i in range(n_items):
        for j in range(i, n_items):
            sim = cosine_similarity(item_user_matrix[i], item_user_matrix[j])
            similarities[i, j] = sim
            if i != j:  # Avoid setting diagonal twice
                similarities[j, i] = sim
    
    return similarities
