from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

from face_detection import get_face_detection

from flask_socketio import SocketIO, send, emit

import json


app = Flask(__name__)
socketio = SocketIO(app)

CORS(app)

@app.route("/")
def serve_main_page():
	return render_template("index.html")


@app.route("/api")
def serve_api():
	print("serving the api......")


# @socketio.on('checkface')
# def check_face(json):
#     #print('received json: ' + str(json))
#     res = get_face_detection(json)
#     emit('checkface_resp', res)


# @socketio.on('is_alive')
# def is_alive_check(data):
# 	emit('is_alive_resp', json.dumps({data: 'SOCKET CONNECTED'}), json=True)
# 	print("Socket connection is alive")



@app.route("/checkface", methods=["POST"])
def check_face():
	return get_face_detection(request)


if __name__ == '__main__':
    socketio.run(app)