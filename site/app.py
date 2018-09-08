from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS

from face_detection import get_face_detection
from face_detection import get_face_detection2

from flask_socketio import SocketIO, send, emit

from FaceDetector import *

import json

from keras.models import load_model

from PIL import Image

import cv2

app = Flask(__name__)
socketio = SocketIO(app)

CORS(app)

fd = FaceDetector("model.h5")
fd.load_model()

model = load_model("emotemodel.h5")

global cur_emote_profile

cur_emote_profile = None

@app.route("/game")
def serve_main_page():
	return render_template("index.html")


@app.route("/")
def serve_landing():
	return render_template("landing.html")


# @socketio.on('checkface')
# def check_face(json):
#     #print('received json: ' + str(json))
#     res = get_face_detection(json)
#     emit('checkface_resp', res)


# @socketio.on('is_alive')
# def is_alive_check(data):
# 	emit('is_alive_resp', json.dumps({data: 'SOCKET CONNECTED'}), json=True)
# 	print("Socket connection is alive")

def get_emote_pf(m):
	for i in range(3):
		print("GET EMOTE PF CALLED!!!")
	im = Image.open(m)
	im = np.array(im)[...,:3]
	orig_im = im.copy()
	im[:,:,0], im[:,:,2] = im[:,:,2].copy(), im[:,:,0].copy() # swaps to BGR so opencv doesnt whine

	face_cascade = cv2.CascadeClassifier('classifiers/haarcascade_frontalface_default.xml')
	gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	if len(faces) == 0:
		print(15*"BIG BAD THING HAPPENED UH OH\n")
		return None

	target_face = faces[0]

	target_face = (target_face[0], target_face[1], target_face[2], int(1.05*target_face[3]))
	target_face_center = (target_face[0] + target_face[2]//2, target_face[1] + target_face[3]//2)
	face_size = int(1.05*max(target_face[2:]))
	loc = (target_face_center[1] - face_size//2, target_face_center[0] - face_size//2)

	face_cropped = orig_im[loc[0]:loc[0]+face_size,loc[1]:loc[1]+face_size]

	face_cropped_small = imresize(face_cropped, (48,48)).astype(np.float64)
	face_cropped_small_gray = 0.15 * face_cropped_small[:,:,0] + 0.65 * face_cropped_small[:,:,1] + 0.2 * face_cropped_small[:,:,2]
	face_emote_ready = face_cropped_small_gray/255.

	pdict = model.predict(face_emote_ready[None,:,:,None])
	kill_me = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
	print("[SERVER IMAGE HERE]")
	for i in range(len(kill_me)):
		print(kill_me[i],"%0.3f"%pdict[0,i])

	return pdict



imlist = ["harn.jpg","rosen.png","rosh.jpg", "001.png", "002.jpg", "003.jpg", "004.png", "005.jpg"]

@app.route("/get_target/<num>")
def get_target(num):
	global cur_emote_profile
	imm = "static/img/" + imlist[int(num)]

	print("HELLO? WE'RE IN GET_TARGET NUM")
	cur_emote_profile = get_emote_pf(imm)
	## UPDATE GLOBAL SHIT
	return send_file(imm, mimetype="image/png")

@app.route("/update_to/<num>")
def update_to(num):
	global cur_emote_profile
	imm = "static/img/" + imlist[int(num)]
	cur_emote_profile = get_emote_pf(imm)
	return ""


@app.route("/checkface", methods=["POST"])
def check_face():
	global cur_emote_profile
	print("JAJAJAJA",cur_emote_profile)
	return get_face_detection2(request, fd, model, cur_emote_profile)
	#return get_face_detection(request)


if __name__ == '__main__':
    socketio.run(app)