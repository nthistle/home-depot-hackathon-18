from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

from face_detection import get_face_detection

app = Flask(__name__)

CORS(app)

@app.route("/")
def serve_main_page():
	return render_template("index.html")


@app.route("/api")
def serve_api():
	print("serving the api......")


@app.route("/checkface", methods=["POST"])
def check_face():
	return get_face_detection(request)
