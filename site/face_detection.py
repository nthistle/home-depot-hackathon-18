import numpy as np
import cv2
import imageio

import base64
import io

import json
from decimal import *
from normalize import *

'''
EmoPY
'''
#import keras
#import lasagne
#import matplotlib
#import scikit-image
#import scikit-learn
#import scikit-neuralnetwork
#import scipy
#import tensorflow
#import opencv-python
#import h5py
#import pydot
#import graphviz


#from fermodel import FERModel

#target_emotions = ['anger', 'fear', 'surprise', 'calm']
#model = FERModel(target_emotions, verbose=True)
from PIL import Image
from keras.models import load_model

from scipy.misc import imresize


def get_face_detection2(request, fd, model, cur_emote_profile):

	b64_str = process_request_to_b64(request)
	bytes_bgr = io.BytesIO(base64.b64decode(b64_str))
	img = imageio.imread(bytes_bgr)

	gimg = request_to_image(request)
	face_cascade = cv2.CascadeClassifier('classifiers/haarcascade_frontalface_default.xml')
	ggray = cv2.cvtColor(gimg, cv2.COLOR_BGR2GRAY)

	faces = face_cascade.detectMultiScale(ggray, 1.3, 5)
	if len(faces) == 0:
		ret = {"face_present":False} #, "image":image_to_b64(gimg)}
		return json.dumps(ret)

	#print("YO THERE IS A FACE")

	target_face = faces[0]
	#target_face = (target_face[0], target_face[1]+int(0.05*target_face[3]), target_face[2], int(1.05*target_face[3]))
	target_face = (target_face[0], target_face[1], target_face[2], int(1.05*target_face[3]))
	target_face_center = (target_face[0] + target_face[2]//2, target_face[1] + target_face[3]//2)
	face_size = int(1.05*max(target_face[2:]))
	loc = (target_face_center[1] - face_size//2, target_face_center[0] - face_size//2)
	#drawn_img = fd.detect_and_draw_loc(img, target_face[:2][::-1], max(target_face[2:]), 2)
	drawn_img = fd.detect_and_draw_loc(img, loc, face_size, 4)

	face_cropped = img[loc[0]:loc[0]+face_size,loc[1]:loc[1]+face_size]

	face_cropped_small = imresize(face_cropped, (48,48)).astype(np.float64)
	face_cropped_small_gray = 0.15 * face_cropped_small[:,:,0] + 0.65 * face_cropped_small[:,:,1] + 0.2 * face_cropped_small[:,:,2]
	face_emote_ready = face_cropped_small_gray/255.

	emodict = {}
	pdict = model.predict(face_emote_ready[None,:,:,None])
	kill_me = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
	for i in range(len(kill_me)):
		print(kill_me[i],"%0.3f"%pdict[0,i])
		emodict[kill_me[i]] = pdict[0,i]
	print()

	
	labels = []
	vals = []
	for key, val in emodict.items():
		labels.append(key)
		vals.append(int(100 * float(val)))



	#Image.fromarray(face_cropped).show()

	#sz = max(target_face[2:])
	#Image.fromarray(face_cropped).show()
	#print(model.predict(face_cropped))


	#drawn_img = fd.detect_and_draw(img, 2)

	drawn_img[:,:,0], drawn_img[:,:,2] = drawn_img[:,:,2].copy(), drawn_img[:,:,0].copy()

	good_stuff = {"face_present":True, "image":image_to_b64(drawn_img), "labs":labels, "vals": vals}

	if not cur_emote_profile is None:
		within_range = 0.1
		in_range_count = 0
		of_possible = 0
		for a,b in zip(pdict[0], cur_emote_profile[0]):
			if b > within_range:
				if abs(a-b) < within_range:
					in_range_count += 1
				else:
					in_range_count += (1 - (abs(a-b)-within_range)) * 0.5
				of_possible += 1
		good_stuff["emote_score"] = (in_range_count / of_possible)
		print("EMOTE_SCORE:",good_stuff["emote_score"])

	return json.dumps(good_stuff)

# return json.dumps({"face_present":True, "image":image_to_b64(drawn_img), "emodictlabels":emodict.keys(), "emodictvals": [x[1] for x in list(emodict.items())]})

def get_face_detection(request):

	img = request_to_image(request)

	face_cascade = cv2.CascadeClassifier('classifiers/haarcascade_frontalface_default.xml')
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	faces = face_cascade.detectMultiScale(gray, 1.3, 5)

	if(len(faces)==1):
		ret = {"face_present": True, "image": None}
		for (x,y,w,h) in faces:
			cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
		ret["image"] = image_to_b64(img)
	else:
		ret = {"face_present": False}

	# faces = [(200, 200, 100, 100)]

	# if(len(faces)==1):
	# 	ret = {"face_present": True, "image": None}
	# 	for (x,y,w,h) in faces:
	# 		cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
	# 	ret["image"] = image_to_b64(img)
	
	return json.dumps(ret)


def process_request_to_b64(request):
	raw_str = request.get_json()["image"]
	front_end_padding = "data:image/png;base64,"
	fin_str = raw_str[len(front_end_padding):]
	return fin_str


def image_to_b64(image):
	_, buff = cv2.imencode('.png', image)
	raw_str = base64.b64encode(buff).decode("utf-8")
	fin_str = "data:image/png;base64," + raw_str
	return fin_str


def request_to_image(request):

	b64_str = process_request_to_b64(request)
	bytes_bgr = io.BytesIO(base64.b64decode(b64_str))

	img = imageio.imread(bytes_bgr)

	#0.15 red, 0.65 green, 0.2 blue

	img2 = img.astype(np.float64)
	img2 = 0.15 * img2[...,0] + 0.65 * img2[...,1] + 0.2 * img2[...,2]


	red = img[:,:,2].copy()
	blue = img[:,:,0].copy()

	img[:,:,0] = red
	img[:,:,2] = blue

	return img