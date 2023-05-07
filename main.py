from flask import Flask, jsonify, request, send_file
import json
import uuid
import cv2
import numpy as np
import os
from imageprocessor import ImageProcessor
from invalidusage import InvalidUsage
import shutil

app = Flask('app')

trashAnalyzer = ImageProcessor()

with open("posts.json", "r") as f:
	posts = json.load(f)

with open("users.json", "r") as f:
	users = json.load(f)

with open("sessions.json", "r") as f:
	sessions = json.load(f)



def authenticate(auth_token):
	authenticated=False
	for session in sessions:
		if session["auth"] == auth_token:
			authenticated=True
	return authenticated

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
	response = jsonify(error.to_dict())
	response.status_code = error.status_code
	return response


@app.route("/")
def hello_world():
	return jsonify({"message": "hello world!"})

@app.route("/image", methods=["POST"])
def process_image():
	# byte file
	print(request.files)
	print(request.form)
	file = request.files['image'].read()
	npimg = np.fromstring(file, np.uint8)
	img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
	if os.path.exists("./results"):
		shutil.rmtree("./results")
	trashAnalyzer.process_image(img)
	return send_file("./results/image0.jpg", mimetype="image/jpg")

@app.route("/login", methods=["POST"])
def login():
	print(request.form)
	for session in sessions:
		if session["username"] == request.form["username"]:
			response = {
				"username": request.form["username"],
				"auth": session["auth"],
				"message": "Already logged in!"
			}
			return jsonify(response), 200

	if request.form["username"] not in users:
		raise InvalidUsage("Not signed up!", status_code=400)

	new_auth = {
		"username": request.form["username"],
		"auth": str(uuid.uuid4())
	}

	sessions.append(new_auth)
	with open("sessions.json", "w") as f:
		json.dump(sessions, f, indent=2)

	new_auth["message"] = "Successfully logged in!"

	return jsonify(new_auth), 200


@app.route("/signup", methods=["POST"])
def signup():
	print(request.form)
	if request.form["username"] == "":
		raise InvalidUsage("Username cannot be empty!", status_code=400)

	if request.form["username"] not in users:
		users.append(request.form["username"])
		with open("users.json", "w") as f:
			json.dump(users, f, indent=2)

	else:
		raise InvalidUsage("Username already exists!", status_code=400)

	return jsonify({"message": "Account Created!"}), 200

@app.route("/posts", methods=["POST", "GET"])
def modify_posts():	

	if (request.method == "POST"):

		if not authenticate(request.form["auth"]):
			raise InvalidUsage("Invalid authentication token!", status_code=400)
		# request form is appended 
		post = {
			"author": request.form["author"],
			"content": request.form["content"],
			"likes": 0
		}
		posts.append(post)

		with open("posts.json", "w") as f:
			json.dump(posts, f, indent=2)
		return jsonify({"message": "Successfully made new post!"}), 200

	if (request.method == "GET"):
		if not authenticate(request.args.get("auth")):
			raise InvalidUsage("Invalid authentication token!", status_code=400)

		return jsonify(posts), 200

	raise InvalidUsage("Invalid method!", status_code=400)

app.run(host='0.0.0.0', port=8080) #ssl_context="adhoc")
