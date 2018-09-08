from keras.models import load_model
from scipy.misc import imresize
import numpy as np
from PIL import Image

class FaceDetector:

	def __init__(self, model_filename):
		self.model_filename = model_filename
		self.model = None

	def load_model(self):
		self.model = load_model(self.model_filename)

	# For this method, img must be RGB 96x96x3
	# Returns the list of keypoints, as predicted directly by the model
	def identify_keypoints(self, img):
		img = img.astype(np.float64)
		img_grayscale = 0.15 * img[:,:,0] + 0.65 * img[:,:,1] + 0.2 * img[:,:,2]
		img_grayscale /= 255.
		#print(img_grayscale.max())
		#print(img_grayscale.min())
		#print(img_grayscale.shape)
		#Image.fromarray(255*img_grayscale).show()
		kp = self.model.predict(img_grayscale[None,:,:,None])[0]
		#print(kp)
		return kp

	# TODO: format these keypoints a bit

	# This is mostly a testing method for now, assumes that img is RGB(A) and 450x600x3(4)
	def detect_and_draw_loc(self, img, loc, face_size, size=3):
		img = np.copy(img[...,:3]) # cut off alpha channel if it exists
		#center_part = img[150:300,225:375] # clip out the center 150x150
		#center_part = img[loc[0]:325,200:400] # clip out the center 150x150
		target_part = img[loc[0]:loc[0]+face_size, loc[1]:loc[1]+face_size]
		kp = self.identify_keypoints(imresize(target_part,(96,96)))
		for kp_x, kp_y in zip(kp[::2],kp[1::2]):
			#kp_x_real = int(225 + 75 + 75 * kp_x)
			#kp_y_real = int(150 + 75 + 75 * kp_y)
			kp_x_real = int(loc[1] + face_size/2 + (face_size/2) * kp_x)
			kp_y_real = int(loc[0] + face_size/2 + (face_size/2) * kp_y)
			try:
				img[kp_y_real-size:kp_y_real+size+1, kp_x_real-size:kp_x_real+size+1] = 255,0,0
			except:
				pass
		img[loc[0]:loc[0]+2,loc[1]:loc[1]+face_size] = 255,0,0
		img[loc[0]+face_size-2:loc[0]+face_size,loc[1]:loc[1]+face_size] = 255,0,0
		img[loc[0]:loc[0]+face_size,loc[1]:loc[1]+2] = 255,0,0
		img[loc[0]:loc[0]+face_size,loc[1]+face_size-2:loc[1]+face_size] = 255,0,0
		return img


	def detect_and_draw(self, img, size=3):
		img = np.copy(img[...,:3]) # cut off alpha channel if it exists
		#center_part = img[150:300,225:375] # clip out the center 150x150
		center_part = img[125:325,200:400] # clip out the center 150x150
		kp = self.identify_keypoints(imresize(center_part,(96,96)))
		for kp_x, kp_y in zip(kp[::2],kp[1::2]):
			#kp_x_real = int(225 + 75 + 75 * kp_x)
			#kp_y_real = int(150 + 75 + 75 * kp_y)
			kp_x_real = int(200 + 100 + 100 * kp_x)
			kp_y_real = int(125 + 100 + 100 * kp_y)
			try:
				img[kp_y_real-size:kp_y_real+size+1, kp_x_real-size:kp_x_real+size+1] = 255,0,0
			except:
				pass
		img[125:127,200:400] = 255,0,0
		img[323:325,200:400] = 255,0,0
		img[125:325,200:202] = 255,0,0
		img[125:325,398:400] = 255,0,0
		#img[150:152,225:375] = 255,0,0
		#img[298:300,225:375] = 255,0,0
		return img



