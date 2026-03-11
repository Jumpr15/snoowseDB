import numpy as np

def euclidean_distance_similarity(x, y):
     return np.sqrt(np.sum(np.square(x - y)))

def dot_product_similarity(x, y):
     return np.sum(np.multiply(x, y))

