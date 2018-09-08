import h5py
import numpy as np

with open("training.csv") as f:
	raw_data = f.read().split("\n")[1:]

data = [x.split("\n") for x in raw_data]
for x in data:
	x[-1] = [int(y) for y in x[-1].split(" ")]