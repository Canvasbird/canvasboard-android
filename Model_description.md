# Model Description

### Steps followed
##### 1. Data Preparation
- 1.1 Scrape Data: The first step was to collect video lectures of professors teaching on the whiteboard. These videos were downloaded from youtube using the Video DownloadHelper extension of Mozilla. 
- 1.2 Trim Videos: The videos were now clipped into smaller videos of 30 seconds using the ffmpeg tool. 
- 1.3 Obtain frames: Each video was now decomposed into frames using ffmpeg. The FPS was set to one. This is done to minimize the occurrence of redundant images.


### 2. Applying the CNN model
#### Define the model

The 'faster_rcnn_inception_v2_coco_2018_01_28' model was used to obtain the detections. This model has a latency of 58 ms for detection. It's fast and it provides accurate results.
Combined with the rest of the processing, this module will display the image in 0.16 seconds on average. 

#### Degree of overlap

The bounding boxes of the person and the white board are passed into this function. The area of intersection is computed along with the area of the person's bounding box. Then the ratio of these areas is computed and returned.
Then if this value is lesser than 0.3, then the whiteboard is cropped from the whole frame and returned in real time. Otherwise, the current frame is omitted.

#### Distortion Correction

The coordinates of the bounding box are passed to this function. Opencv's warpPerspective is used for cropping the frame. This is very flexible and can handle skewed frames as well.
Finally, the image is converted to greyscale. Then adaptive thresholding is applied and then the image is inverted. This enhances the image and increases the lumination.

