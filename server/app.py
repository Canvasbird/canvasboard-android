from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from flask_jwt_extended import (
	JWTManager, jwt_required, create_access_token,
	get_jwt_identity
)
import pymongo
#from flask_socketio import SocketIO, emit
import base64
from io import BytesIO
from PIL import Image
import gc
#from flask import Response

import numpy as np
import tensorflow as tf
# tf.disable_v2_behavior()
import cv2
import time
# from google.colab.patches import cv2_imshow
import os

connectionUrl = "mongodb+srv://rohit:Rohit123@cluster0.qj7jq.mongodb.net/canvasboard?retryWrites=true&w=majority"
myclient = pymongo.MongoClient(connectionUrl)

db = myclient["canvasboard"]
collection = db["users"]

class DetectorAPI:
    def __init__(self, path_to_ckpt):
        #Initialize the file path of the model checkpoint
        self.path_to_ckpt = path_to_ckpt

        #Initializing the basic computation graph of tensorflow
        self.detection_graph = tf.Graph()
        with self.detection_graph.as_default():
            od_graph_def = tf.compat.v1.GraphDef()
            with tf.compat.v2.io.gfile.GFile(self.path_to_ckpt, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')
        self.default_graph = self.detection_graph.as_default()

        #Creating a session
        self.sess = tf.compat.v1.Session(graph=self.detection_graph)

        # Definite input and output Tensors for detection_graph
        self.image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')

        # Each box represents a part of the image where a particular object was detected.
        self.detection_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')

        # Each score represent the level of confidence for each of the objects.
        self.detection_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')

        # Each class represents different entities that were detected
        self.detection_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')

        # The total no of detections that were computed in the image
        self.num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')


    def processFrame(self, image):
        # Expand dimensions since the trained_model expects images to have shape: [1, None, None, 3]
        image_np_expanded = np.expand_dims(image, axis=0)
        # Actual detection.
        (boxes, scores, classes, num) = self.sess.run(
            [self.detection_boxes, self.detection_scores, self.detection_classes, self.num_detections],
            feed_dict={self.image_tensor: image_np_expanded})

        #Unpack the shape of the image
        im_height, im_width,_ = image.shape

        boxes_list = [None for i in range(boxes.shape[1])]
        for i in range(boxes.shape[1]):
            boxes_list[i] = (int(boxes[0,i,0] * im_height),
                        int(boxes[0,i,1]*im_width),
                        int(boxes[0,i,2] * im_height),
                        int(boxes[0,i,3]*im_width))

        # boxes_list -> Contains the coordinates of the bounding rectangular box for every class
        # scores -> List of confidence score for each detection
        # classes -> List of classes detected
        # num -> total number of detections in the image

        return boxes_list, scores[0].tolist(), [int(x) for x in classes[0].tolist()], int(num[0])

    def close(self):
        #Closing the session
        self.sess.close()
        #Closing the computuation graph
        self.default_graph.close()

def degree_of_overlap(boxA, boxB):
    # determine the (x, y)-coordinates of the intersection rectangle
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    # compute the area of intersecting rectangle
    interArea = abs(max((xB - xA, 0)) * max((yB - yA), 0))
    if interArea == 0:
        return 0

    # Compute the area of boxB
    boxBArea = abs((boxB[2] - boxB[0]) * (boxB[3] - boxB[1]))

    # Determine the ratio of the overlapping area to that of boxBArea
    overlap = interArea / float(boxBArea)

    return overlap

def distortionCorrection(img,corners):
    M,N,_ = img.shape
    # finding homography matrix.
    aux=cv2.getPerspectiveTransform(corners,np.float32([[0,0],[N,0],[N,M],[0,M]]))

    # Use the homography matrix to crop the image.
    img1 = cv2.warpPerspective(img,aux,(N,M))

    # converting image to greyscale
    img1grey=cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

    # enhancing the image via adaptive thresholding
    img2=cv2.adaptiveThreshold(img1grey,255,1,1,7,2)

    # inverting the image so that the contents will be black on a white background.
    img2=cv2.bitwise_not(img2)

    return img2




app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'rohit'
app.config['JWT_SECRET_KEY'] = 'qmxgrstf234rfdxfgtrs!@#'
jwt = JWTManager(app)
#socketio = SocketIO(app,cors_allowed_origins="*")

@app.route('/')
def home_page():
	return render_template('index.html')

@app.route('/classes', methods=['POST'])
@jwt_required
def get_classlist():
	current_user = get_jwt_identity()
	id = current_user["_id"]
	classesCollection = db[f"{id}"]
	classes = classesCollection.find({})

	response = []
	for class_ in classes:
		class_["_id"] = str(class_["_id"])
		response.append(class_)
	return jsonify(response) 

@app.route('/schedule', methods=['POST'])
@jwt_required
def schedule_class():
	data = request.get_json()
	print(data)
	current_user = get_jwt_identity()
	id = current_user["_id"]
	classCollection = db[f"{id}"]
	subject = data.get("subject", "")
	facultyName = data.get("faculty_name", "")
	dateTime = data.get("date_time", "")

	data = {
		"subject":subject,
		"faculty_name":facultyName,
		"date_time":dateTime
	}

	class_ = classCollection.insert_one(data)
	inserted_id = str(class_.inserted_id)

	return jsonify({
		"class_id":inserted_id
	})

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


def split_up_resize(arr, res):
    """
    function which resizes large array (direct resize yields error (addedtypo))
    """

    # compute destination resolution for subarrays
    res_1 = (res[0], res[1]/2)
    res_2 = (res[0], res[1] - res[1]/2)

    # get sub-arrays
    arr_1 = arr[0 : len(arr)/2]
    arr_2 = arr[len(arr)/2 :]

    # resize sub arrays
    arr_1 = cv2.resize(arr_1, res_1, interpolation = cv2.INTER_LINEAR)
    arr_2 = cv2.resize(arr_2, res_2, interpolation = cv2.INTER_LINEAR)

    # init resized array
    arr = np.zeros((res[1], res[0]))

    # merge resized sub arrays
    arr[0 : len(arr)/2] = arr_1
    arr[len(arr)/2 :] = arr_2

    return arr

@app.route('/process', methods=['POST'])
def image_process():
	model_path = 'faster_rcnn_inception_v2_coco_2018_01_28/frozen_inference_graph.pb'
	odapi = DetectorAPI(path_to_ckpt=model_path)
	data = request.data
	type_, data = data.split(b',')
	img = data
	img = base64.b64decode(img)
	img = np.fromstring(img, dtype=np.uint8)
	img = cv2.imdecode(img, 1)
	threshold = 0.7
	# img = BytesIO(img)
	# img = np.array(Image.open(img))#.convert('LA')
	
	# img = np.expand_dims(img, axis=0)
	# img = np.array(img)
	#Resize the image

	img = cv2.resize(img, (640,480))
	# img = split_up_resize(img, (640, 480))

	#Send the image to the detection module
	boxes, scores, classes, num = odapi.processFrame(img)

	#Variable which determines whether to omit the current frame or not.
	omit=0

	#This indicates the status of board detection
	detect_board=False

	box1=[80,32,415,332]
	corners=np.float32([[box1[0],box1[1]],[box1[2],box1[1]],[box1[2],box1[3]],[box1[0],box1[3]]])

	#Iterate over the bounding boxes of each class
	for i in range(len(boxes)):
	  # If a person is detected and the confidence score is above the threshold, then enter the if condition.
	  if classes[i] == 1 and scores[i] > threshold:
	      #Select the ith box
	      box = boxes[i]

	      #Expand the ith box to obtain the minimum and maximum x and y coordinates of the person detected
	      box2=[box[1],box[0],box[3],box[2]]

	      #Find the degree of overlap between the white board and the person
	      overlap=degree_of_overlap(box1,box2)

	      #Round it off to relax the condition.
	      overlap=round(overlap,1)

	      #If the overlap is higher than 0.3, then the person is obstructing a good chunk of the board.
	      #Omit this frame and wait for the next frame.
	      if(overlap>0.3):
	        #Set the omit variable to 1.
	        omit=1

	#omit is 0 implies, frame should not be omitted
	if (omit==0):
	#Send the current frame along with corners of the white board for cropping
		image2 = distortionCorrection(img,corners)
		# image2 = Image.fromarray(image2)
		# img = BytesIO()
		# image2.save(img, format="PNG")
		retval, buffer = cv2.imencode('.png', image2)
		img_str = base64.b64encode(buffer)
		gc.collect()
		return jsonify({
			"image":type_.decode()+','+img_str.decode()
		})
	else:
		# img_ = BytesIO()
		# cv2.imwrite(img_, img)
		retval, buffer = cv2.imencode('.png', img)
		img_str = base64.b64encode(buffer)
		gc.collect()
		return jsonify({
			"image":type_.decode()+','+img_str.decode()
		})
	


if __name__ == '__main__':
	#socketio.run(app, debug=True, host='0.0.0.0', port=8000)
	app.run(debug=True, host='0.0.0.0', port=5000)
