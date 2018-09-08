import h5py
import numpy as np

with open("training.csv") as f:
	raw_data = f.read().split("\n")[1:]

print("Opened training data in csv format.")
data = [x.split(",") for x in raw_data if len(x) > 1]
print("Split training data.")
#ndata = []
#for x in data:


for x in data:
	x[-1] = [int(y) for y in x[-1].split(" ")]

print(f"Parsed {len(data)} images with labels from training.csv")

with h5py.File("training_data.hdf5","w") as f:
	img_dataset = f.create_dataset("images", (len(data), 96, 96), np.uint8)

	for i in range(len(data)):
		img_dataset[i] = np.reshape(data[i][-1], (96, 96))

	print("Images loaded into hdf5 file.")

	lbl_dataset = f.create_dataset("labels", (len(data), 30), np.float64)

	print(data[0][:30])
	print(data[-1][:30])
	print(data[5550][:30])

	for i in range(len(data)):
		break
		try:
			lbl_dataset[i] = np.array([float(x) for x in data[i][:30]])
		except:
			print(i)

	print("Labels loaded into hdf5 file.")



print("Done! Data converted to hdf5 format.")
