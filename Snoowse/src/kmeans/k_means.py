from sklearn.cluster import KMeans
import numpy as np

class KMean_Cluster():
     def __init__(self, n_clusters):
          self.kmeans = KMeans(
               n_clusters=n_clusters
          )
          
     def fit(self, vector_list: list[np.ndarray]):
          cluster_list = self.kmeans.fit(vector_list)
          return cluster_list.labels_
     
     def predict(self, vector: np.ndarray):
          return self.kmeans.predict(vector)
     
          