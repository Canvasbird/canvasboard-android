#Import the following packages

import numpy as np
import tensorflow as tf
# tf.disable_v2_behavior()
import cv2
import time
import os

#Create a class for detection
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

if __name__== '__main__' :
    #load model from file path
    model_path = 'faster_rcnn_inception_v2_coco_2018_01_28/frozen_inference_graph.pb'

    #Pass the model path to the detection class and initialize the model
    odapi = DetectorAPI(path_to_ckpt=model_path)

    #Set the threshold. This is useful for filtering the results based on the confidence score.
    threshold=0.7

    #Initialize a dictionary to store the processed frames
    img_dict={}

    # Stores count of the frames that are valid
    valid_image=0

    #This indicates the status of board detection
    detect_board=False

    #iterate over the image folder
    for img_path in sorted(os.listdir('img')):

        #read the image from the folder
        img=cv2.imread('img/'+img_path)

        #Resize the image
        img = cv2.resize(img, (640,480))

        #Initialize the start time for the detection
        start_time = time.time()

        #Send the image to the detection module
        boxes, scores, classes, num = odapi.processFrame(img)

        #Variable which determines whether to omit the current frame or not.
        omit=0

        #Iterate over the bounding boxes of each class
        for i in range(len(boxes)):
          # If a board is detected and the confidence score is above the threshold, then enter the if condition
          if classes[i] == 2 and scores[i] > threshold and detect_board == False:
              #Set detect_board to true
              detect_board = True

              #Select the ith box
              box = boxes[i]

              #Expand the ith box to obtain the minimum and maximum x and y coordinates of the person detected
              box1=[box[1],box[0],box[3],box[2]]

              #Determin the four corners of the white board
              corners=np.float32([[box1[0],box1[1]],[box1[2],box1[1]],[box1[2],box1[3]],[box1[0],box1[3]]])

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

        # Initialize the end time
        end_time = time.time()

        #Useful for computing the latency for each frame
        print("Elapsed Time:", end_time-start_time)

        #omit is 0 implies, frame should not be omitted
        if (omit==0):
          #Send the current frame along with corners of the white board for cropping
          image2=distortionCorrection(img,corners)

          #Store the resuting image in a dictionary
          img_dict[valid_image]=image2

          # Update valid_image
          valid_image=valid_image+1

    # Save the images in the outout directory
    for k in img_dict.keys():
        cv2.imwrite('out/image'+str(k)+'.png',img_dict[k])
