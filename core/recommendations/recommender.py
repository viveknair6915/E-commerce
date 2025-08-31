""
Advanced recommender system with Cython-optimized similarity calculations.
"""
import numpy as np
from typing import List, Dict, Tuple, Optional
import logging

# Import Cython-optimized functions
try:
    from .similarity import cosine_similarity, calculate_similarities
    CYTHON_AVAILABLE = True
except ImportError:
    CYTHON_AVAILABLE = False
    logging.warning("Cython extensions not found. Using pure Python implementation.")

class Recommender:
    """Hybrid recommender system with Cython optimizations."""
    
    def __init__(self, use_cython: bool = True):
        self.user_item_matrix = None
        self.similarities = None
        self.id_maps = {}
        self.reverse_maps = {}
        self.use_cython = use_cython and CYTHON_AVAILABLE
    
    def fit(self, interactions: List[Tuple[int, int, float]]) -> None:
        """Fit model with user-item interactions."""
        if not interactions:
            raise ValueError("No interactions provided")
            
        # Create mappings
        user_ids = {uid for uid, _, _ in interactions}
        item_ids = {iid for _, iid, _ in interactions}
        
        self.id_maps['user'] = {uid: i for i, uid in enumerate(user_ids)}
        self.id_maps['item'] = {iid: i for i, iid in enumerate(item_ids)}
        
        # Initialize matrix
        n_users = len(self.id_maps['user'])
        n_items = len(self.id_maps['item'])
        self.user_item_matrix = np.zeros((n_users, n_items))
        
        # Fill matrix
        for uid, iid, rating in interactions:
            u = self.id_maps['user'][uid]
            i = self.id_maps['item'][iid]
            self.user_item_matrix[u, i] = rating
        
        self._calculate_similarities()
    
    def _calculate_similarities(self):
        """Calculate item similarities."""
        if self.use_cython:
            self.similarities = calculate_similarities(self.user_item_matrix.T)
        else:
            # Pure Python fallback
            n_items = self.user_item_matrix.shape[1]
            self.similarities = np.zeros((n_items, n_items))
            for i in range(n_items):
                for j in range(i, n_items):
                    sim = self._cosine_sim(
                        self.user_item_matrix[:, i],
                        self.user_item_matrix[:, j]
                    )
                    self.similarities[i, j] = sim
                    self.similarities[j, i] = sim
    
    def _cosine_sim(self, u, v):
        """Cosine similarity between two vectors."""
        dot = np.dot(u, v)
        norm_u = np.linalg.norm(u)
        norm_v = np.linalg.norm(v)
        return dot / (norm_u * norm_v) if norm_u > 0 and norm_v > 0 else 0.0
    
    def recommend(
        self, 
        user_id: int, 
        n: int = 5, 
        min_similarity: float = 0.0
    ) -> List[Tuple[int, float]]:
        """Generate item recommendations for a user."""
        if user_id not in self.id_maps['user']:
            return []
            
        user_idx = self.id_maps['user'][user_id]
        user_ratings = self.user_item_matrix[user_idx]
        rated_items = set(np.where(user_ratings > 0)[0])
        
        # Calculate predicted ratings
        predicted = np.zeros(self.user_item_matrix.shape[1])
        
        for item_idx in range(self.user_item_matrix.shape[1]):
            if item_idx in rated_items:
                continue
                
            # Find similar items that the user has rated
            sim_items = [
                (i, sim) 
                for i, sim in enumerate(self.similarities[item_idx])
                if i in rated_items and sim > min_similarity
            ]
            
            if not sim_items:
                continue
                
            # Calculate weighted average
            sum_sim = sum(sim for _, sim in sim_items)
            if sum_sim > 0:
                weighted_sum = sum(user_ratings[i] * sim for i, sim in sim_items)
                predicted[item_idx] = weighted_sum / sum_sim
        
        # Get top N recommendations
        item_scores = [
            (list(self.id_maps['item'].keys())[i], score)
            for i, score in enumerate(predicted)
            if i not in rated_items and score > 0
        ]
        
        return sorted(item_scores, key=lambda x: x[1], reverse=True)[:n]
