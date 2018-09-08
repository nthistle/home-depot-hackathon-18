import numpy as np
import cv2
import imageio

import base64
import io

import json

'''
EmoPY
'''
import keras
import lasagne
import matplotlib
import scikit-image
import scikit-learn
import scikit-neuralnetwork
import scipy
import tensorflow
import opencv-python
import h5py
import pydot
import graphviz

def get_face_detection2(request, fd):

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
	drawn_img = fd.detect_and_draw_loc(img, target_face[:2][::-1], max(target_face[2:]), 2)

	#drawn_img = fd.detect_and_draw(img, 2)

	drawn_img[:,:,0], drawn_img[:,:,2] = drawn_img[:,:,2].copy(), drawn_img[:,:,0].copy()
	return json.dumps({"face_present":True, "image":image_to_b64(drawn_img)})


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