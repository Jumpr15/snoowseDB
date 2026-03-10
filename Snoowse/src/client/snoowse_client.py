import shutil
import zarr
import numpy as np

from similarity_search.search import euclidean_distance_similarity, dot_product_similarity

class Snoowse_Client:
     def __init__(self):
          pass
     
     def create_collection(self, collection_name):
          try: 
               collection = zarr.create_group(
                    store=f"{collection_name}.zarr"
               )
               
               return collection
               
          except Exception as e:
               print(f"Error while creating collection: {e}")
               return e
          
     def delete_collection(self, collection_name):
          try:
               shutil.rmtree(
                    f"{collection_name}.zarr"
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
                    store=f"{collection_name}.zarr",
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