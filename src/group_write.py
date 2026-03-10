import zarr

group = zarr.create_group(store="group.zarr")
arr1 = group.create_array(name="arr1", shape=(10, 10), dtype="f4")
arr2 = group.create_array(name="arr2", shape=(4, 8), dtype="f4")

print(group)
