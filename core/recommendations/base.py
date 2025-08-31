"""
Base recommendation system implementation using collaborative filtering.
"""
import numpy as np
from collections import defaultdict
from typing import List, Dict, Tuple

class BaseRecommender:
    """Base class for recommendation systems."""
    
    def __init__(self):
        self.user_item_matrix = None
        self.user_similarities = None
        self.item_similarities = None
        self.user_id_map = {}
        self.item_id_map = {}
        self.reverse_user_map = {}
        self.reverse_item_map = {}
    
    def fit(self, interactions: List[Tuple[int, int, float]]) -> None:
        """
        Fit the model with user-item interactions.
        
        Args:
            interactions: List of (user_id, item_id, rating) tuples
        """
        # Create mappings for user and item IDs to matrix indices
        user_ids = {user_id for user_id, _, _ in interactions}
        item_ids = {item_id for _, item_id, _ in interactions}
        
        self.user_id_map = {user_id: i for i, user_id in enumerate(user_ids)}
        self.item_id_map = {item_id: i for i, item_id in enumerate(item_ids)}
        self.reverse_user_map = {v: k for k, v in self.user_id_map.items()}
        self.reverse_item_map = {v: k for k, v in self.item_id_map.items()}
        
        # Initialize user-item matrix
        n_users = len(self.user_id_map)
        n_items = len(self.item_id_map)
        self.user_item_matrix = np.zeros((n_users, n_items))
        
        # Fill the user-item matrix
        for user_id, item_id, rating in interactions:
            user_idx = self.user_id_map[user_id]
            item_idx = self.item_id_map[item_id]
            self.user_item_matrix[user_idx, item_idx] = rating
    
    def calculate_similarity(self, u: np.ndarray, v: np.ndarray) -> float:
        """
        Calculate cosine similarity between two vectors.
        
        Args:
            u: First vector
            v: Second vector
            
        Returns:
            float: Cosine similarity between u and v
        """
        # Avoid division by zero
        norm_u = np.linalg.norm(u)
        norm_v = np.linalg.norm(v)
        
        if norm_u == 0 or norm_v == 0:
            return 0.0
            
        return np.dot(u, v) / (norm_u * norm_v)
    
    def get_user_similarities(self) -> np.ndarray:
        """
        Calculate user-user similarity matrix.
        
        Returns:
            np.ndarray: User similarity matrix
        """
        if self.user_similarities is not None:
            return self.user_similarities
            
        n_users = self.user_item_matrix.shape[0]
        self.user_similarities = np.zeros((n_users, n_users))
        
        for i in range(n_users):
            for j in range(i, n_users):
                sim = self.calculate_similarity(
                    self.user_item_matrix[i],
                    self.user_item_matrix[j]
                )
                self.user_similarities[i, j] = sim
                self.user_similarities[j, i] = sim
                
        return self.user_similarities
    
    def get_item_similarities(self) -> np.ndarray:
        """
        Calculate item-item similarity matrix.
        
        Returns:
            np.ndarray: Item similarity matrix
        """
        if self.item_similarities is not None:
            return self.item_similarities
            
        n_items = self.user_item_matrix.shape[1]
        self.item_similarities = np.zeros((n_items, n_items))
        
        for i in range(n_items):
            for j in range(i, n_items):
                sim = self.calculate_similarity(
                    self.user_item_matrix[:, i],
                    self.user_item_matrix[:, j]
                )
                self.item_similarities[i, j] = sim
                self.item_similarities[j, i] = sim
                
        return self.item_similarities
    
    def recommend_items(self, user_id: int, n: int = 5) -> List[Tuple[int, float]]:
        """
        Recommend items to a user.
        
        Args:
            user_id: ID of the user to recommend items to
            n: Number of recommendations to return
            
        Returns:
            List of (item_id, score) tuples, sorted by score in descending order
        """
        raise NotImplementedError("Subclasses must implement this method")
    
    def batch_recommend(self, user_ids: List[int], n: int = 5) -> Dict[int, List[Tuple[int, float]]]:
        """
        Recommend items to multiple users.
        
        Args:
            user_ids: List of user IDs to recommend items to
            n: Number of recommendations per user
            
        Returns:
            Dictionary mapping user IDs to lists of (item_id, score) tuples
        """
        return {user_id: self.recommend_items(user_id, n) for user_id in user_ids}
