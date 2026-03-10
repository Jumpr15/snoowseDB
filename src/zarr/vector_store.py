import zarr
import numpy as np
from uuid import uuid4

class vector_store:
     def __init__(self, name, dtype):
          self.dtype = dtype
          self.vector_store = zarr.create_group(store=f"{name}.zarr")
          
     
     def add_vector(self, name, vector: np.ndarray): # vector must be np array
          arr = self.vector_store.create_array(
               name=name,
               shape=vector.shape,
               dtype=self.dtype
          )
          
store = vector_store("store", "f2")
store.add_vector(
     "happy",
     np.array([5, 3, 6, 6, 2])
)

