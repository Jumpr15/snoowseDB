import zarr
import numpy as np

group = zarr.open_group(store="group.zarr")

for name, arr in group.arrays():
     print(name, arr.shape, arr)