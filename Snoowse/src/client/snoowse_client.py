import shutil
import zarr
import numpy as np

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