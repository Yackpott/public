import numpy as np

# zeros, ones, empty
a = np.zeros(5,4, dtype=np.int_)
print(a)
# dimensions
print(len(a))
# number of elements
print(a.size)

# random.rand(5,4) or random.randint random.normal
a = np.random.normal(50,10, size=(5,4))

a = np.random.randint(0,10, size=(5,4))

# axis=0 for columns axis=1 for rows
# a.max() and a.min()
a.sum(axis=0)

# slicing rows, columns
a[0, 2:4]

# array indices
indices = np.array([1,2,3,4])
print(a[indices])

#masking

mean = a.mean()
print(a[a<mean])

# a/2 output of int, a/2.0 output of float
# np.dot matrix mult