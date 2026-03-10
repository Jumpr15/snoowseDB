# euclidean distance: root(sum(element wise subtraction)^2))

import numpy as np

a = np.array([6, 7, 8])
b = np.array([1, 2, 3])

# c = a - b
# d = np.square(c)
# e = np.sum(d)
# f = np.sqrt(e)

def euclidean_distance_similarity(x, y):
     return np.sqrt(np.sum(np.square(x - y)))

def dot_product_similarity(x, y):
     return np.sum(np.multiply(x, y))

print(euclidean_distance_similarity(a, b))
print(dot_product_similarity(a, b))