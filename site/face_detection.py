import numpy as np
import cv2
import imageio

import base64
import io

import json


def get_face_detection(request):

	img = request_to_image(request)

	face_cascade = cv2.CascadeClassifier('classifiers/haarcascade_frontalface_default.xml')
	eye_cascade = cv2.CascadeClassifier('classifiers/haarcascade_eye.xml')
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	faces = face_cascade.detectMultiScale(gray, 1.3, 5)

	if(len(faces)==1):
		ret = {"face_present": True}
	else:
		ret = {"face_present": False}
	
	return json.dumps(ret)


def process_request_to_b64(request):
	raw_str = request.get_json()["image"]
	front_end_padding = "data:image/png;base64,"
	fin_str = raw_str[len(front_end_padding):]
	return fin_str


def request_to_image(request):

	b64_str = process_request_to_b64(request)
	bytes_bgr = io.BytesIO(base64.b64decode(b64_str))

	img = imageio.imread(bytes_bgr)

	red = img[:,:,2].copy()
	blue = img[:,:,0].copy()

	img[:,:,0] = red
	img[:,:,2] = blue

	return img