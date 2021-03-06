from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import (
	JWTManager, jwt_required, create_access_token,
	get_jwt_identity
)
import pymongo
import base64
from io import BytesIO
from PIL import Image
import gc

connectionUrl = "mongodb+srv://rohit:Rohit123@cluster0.qj7jq.mongodb.net/canvasboard?retryWrites=true&w=majority"
myclient = pymongo.MongoClient(connectionUrl)

db = myclient["canvasboard"]
collection = db["users"]

app = Flask(__name__)
CORS(app)

app.config['JWT_SECRET_KEY'] = 'qmxgrstf234rfdxfgtrs!@#'
jwt = JWTManager(app)

#current_user = get_jwt_identity()


@app.route('/login', methods=['POST'])
def login():
	if not request.is_json:
		return jsonify({"message":"SEND JSON request"}), 400
	
	email = request.json.get("email", None)
	password = request.json.get("password", None)
	
	if not email:
		return jsonify({"msg":"email required"}), 400
	if not password:
		return jsonify({"msg":"password required"}), 400
	
	user = collection.find_one({"email":email, "password":password}, {})
	
	if not user:
		return jsonify({"msg":"invalid user"}), 404
		
	user["_id"] = str(user["_id"])
	access_token = create_access_token(identity=user)
	return jsonify(access_token=access_token)

@app.route('/register', methods=['POST'])
def register():
	data = request.get_json()
	username = data.get("username", None)
	email = data.get("email", None)
	password = data.get("password", None)
	
	#find user
	user = collection.find_one({"email":email},{})
	print(user)
	if user == email:
		return jsonify({"msg":"email already taken"}), 400
	#register user
	
	if not username:
		return jsonify({"msg":"provide username"}), 400
	
	if not password:
		return jsonify({"msg":"provide password"}), 400
	
	if not email:
		return jsonify({"msg":"provide email"}), 400
	
	user = {"username":username, "email":email, "password":password}
	user = collection.insert_one(user)
	#user.inserted_id = str(user.inserted_id)
	
	return jsonify({"user":str(user.inserted_id)})


@app.route('/process', methods=['POST'])
def image_process():
	data = request.data
	type_, data = data.split(b',')
	image = data
	image = base64.b64decode(image)
	image = BytesIO(image)
	image = Image.open(image).convert('LA') # this is a colored image if needed convert it into gray scale
	
	## start your ML code here using above image ##
	
	image_output = image # <---------- output image goes here
	## end of ML code ##
	
	img = BytesIO()
	image_output.save(img, format="PNG")
	img_str = base64.b64encode(img.getvalue())
	
	gc.collect()
	return jsonify({
		"image":type_.decode()+','+img_str.decode()
	})

if __name__ == '__main__':
	app.run(debug=True)
