from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
app = Flask(__name__)

CORS(app)

@app.route("/")
def serve_main_page():
	return "wow look at this page"


