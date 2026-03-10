from snoowse_client import Snoowse_Client
import numpy as np

snoowse = Snoowse_Client()

x = np.array([1, 2, 3])
y = np.array([2, 4, 6])
z = np.array([15, 24, 33])

collection_name = "snoowsedb"

collection = snoowse.create_collection(collection_name)
doc1 = snoowse.insert_document(collection_name, "test1", x)
doc2 = snoowse.insert_document(collection_name, "test2", y)
doc3 = snoowse.insert_document(collection_name, "test3", z)

try: 
     arr_res = snoowse.euclidean_similarity_search(collection, x)
     for res in arr_res:
          print(res)

finally:     
     snoowse.delete_collection(collection_name)