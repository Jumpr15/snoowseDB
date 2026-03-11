import shutil
import zarr
import string
import random
import numpy as np

from similarity_search.search import euclidean_distance_similarity, dot_product_similarity
from kmeans.k_means import KMean_Cluster

class Snoowse_Client:
     def __init__(self, n_clusters:int = 3):
          self.n_clusters = n_clusters
          self.kmeans = KMean_Cluster(self.n_clusters)
     
     def create_collection(self, collection_name):
          try: 
               collection = zarr.create_group(
                    store=f"{collection_name}"
               )
               
               return collection
               
          except Exception as e:
               print(f"Error while creating collection: {e}")
               return e
     
     def get_collection(self, root_collection_name, collection_name):
          try: 
               res = zarr.open_group(
                    store=f"{root_collection_name}",
                    mode="r",
                    path=collection_name
               )
               
               return res
               
          except Exception as e:
               print(f"Error while getting collection: {e}")
               return e     
     
     def insert_collection(self, root_collection_name, collection_name):
          try: 
               res = zarr.open_group(
                    store=f"{root_collection_name}",
                    mode="w",
                    path=collection_name
               )
               
               return res
               
          except Exception as e:
               print(f"Error while inserting collection: {e}")
               return e     
          
     def delete_collection(self, collection_name):
          try:
               shutil.rmtree(
                    f"{collection_name}"
               )
          
          except Exception as e:         
               print(f"Error while deleting collection: {e}")
               return e
          
     def get_document_by_name(self, collection_name, vector_name):
          try:
               res = zarr.open_array(
                    store=f"{collection_name}.zarr",
                    mode="r",
                    path=vector_name
               )
               
               return res
          
          except Exception as e:
               print(f"Error while getting vector: {e}")
               return e
          
     def insert_document(self, collection_name, vector_name, vector: np.ndarray):
          try: 
               res = zarr.open_array(
                    store=f"{collection_name}",
                    mode="w",
                    path=vector_name,
                    shape=vector.shape
               )
               
               res[...] = vector
               
               return res
               
          except Exception as e:
               print(f"Error while inserting vector: {e}")
               return e          
              
     ### fixed array size for write
     def update_document(self, collection_name, vector_name, new_vector: np.ndarray):
          try:
               res = zarr.open_array(
                    store=f"{collection_name}.zarr",
                    mode="r+",
                    path=vector_name   
               )
               
               res[...] = new_vector
               
               return res
          
          except Exception as e:
               print(f"Error while updating vector: {e}")
               return e                         
          
     def delete_document(self, collection_name, vector_name):
          try:
               group = zarr.open_group(
                    store=f"{collection_name}.zarr",
                    mode="a"
               )
               
               del group[vector_name]
               
          except Exception as e:
               print(f"Error while deleting vector: {e}")
               return e                 
           
     def euclidean_similarity_search(self, collection, target):
          res = []
          for name, vector in collection.arrays():
               res.append({
                    "vector_name": name,
                    "vector_value": vector,
                    "search_method": "euclidean_distance",
                    "similarity_value": euclidean_distance_similarity(vector, target)
               })
               
          return res
               
     def dp_similarity_search(self, collection, target):
          res = []
          for name, vector in collection.arrays():
               res.append({
                    "vector_name": name,
                    "vector_value": vector,
                    "search_method": "dot_product",
                    "similarity_value": dot_product_similarity(vector, target)
               })
               
          return res
     
     def id_generator(self, size=6, chars=string.ascii_letters + string.digits):
          return ''.join(random.choice(chars) for i in range(size))
     
     # setup ivf
     def cluster_setup(self, collection, documents: list[np.ndarray]):
          for i in range(self.n_clusters):
               self.insert_collection(collection, f"c{i}")
               
          label_list = self.kmeans.fit(documents)
          
          for index, doc in zip(label_list, documents):
               print(f"{index}: {doc} - {self.id_generator()}")
               self.insert_document(f"{collection}/c{index}", f"{self.id_generator()}", doc)
          
     def document_ingestion(self, collection, document: np.ndarray):
          index = int(self.kmeans.predict([document])[0])
          self.insert_document(f"{collection}/c{index}", f"{self.id_generator()}", document)
          
     def cluster_search(self, collection, target: np.ndarray):
          index = int(self.kmeans.predict([target])[0])
               
          collection_ref = self.get_collection(collection, f"c{index}")
               
          res = self.euclidean_similarity_search(
               collection_ref,
               target
          )
          
          return res