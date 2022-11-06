# Description: A python file storing the necessary codes to be used in train.py and test.py files.
# In this project, we are making use of Detectron2 developed by FAIR.
# Credits to Detetcron2 developers:
#                        authors =      Yuxin Wu and Alexander Kirillov and Francisco Massa and Wan-Yen Lo and Ross Girshick
#                        title  =       Detectron2
#                        url    =       https://github.com/facebookresearch/detectron2
#                        year   =       2019


# This code is being run Python 3.9.7 version, Macbook Pro, Chip Apple M1, MacOS Monterey, version 12.3.1


# Importing necessary libraries from Detetctron2
from detectron2 import model_zoo        # To load pretrained models
# To load the configuration for object detection model
from detectron2.config import get_cfg
# To visualise the images
from detectron2.utils.visualizer import Visualizer, ColorMode
from detectron2.data import MetadataCatalog, DatasetCatalog

# Importing libraries for image/video processing
import random
import cv2 as cv
import matplotlib.pyplot as plt
# import roboticarm

# Using time to pause the loops
import time

# Importing Pyrealsense Processing libraries
# import pyrealsense2
# from realsense_depth import *

# A function that visualise the annotations on images given as samples to verify images are
# correctly registered with the annotations.
# Parameters: datasetName --> Name given to the dataset
#             number --> number of images you want to plot. Custom is 1.


def plottingSamples(datasetName, number=1):

    sampleMetadata = MetadataCatalog.get(datasetName)    # To get metadata
    datasetDicts = DatasetCatalog.get(datasetName)     # To get datasets

    # Getting randome sample for verifications
    for s in random.sample(datasetDicts, number):
        # Reading images
        img = cv.imread(s["file_name"])
        # Initialise the visualizer and pass the image in the visualiser
        visualizer = Visualizer(
            img[:, :, ::-1], metadata=sampleMetadata, scale=0.5)
        # Drawing the annotations on the iamge
        vis = visualizer.draw_dataset_dict(s)
        # Plotting the image into a figure
        plt.figure(figsize=(15, 20))
        plt.imshow(vis.get_image())
        plt.show()


# A function that is used to define the configuration being used in training of the model
# Parameters: pathForConfigFile --> A path to config file .i.e. URL
#             pathForCheckpointURL --> A path to weights and checkpoints .i.e. URL
#             trainingDatasetName  --> Name given to the dataset that is being trained
#             testDatasetName --> Name given to the test dataset that is being used
#             classesNumber --> Number of classes being used in training the model
#             outputDirectory --> The directory where you are going to store the trained model files
#             device --> The system that you are using .i.e. cpu or cuda (cuda is used on gpu)
# Returns:    cfg --> A customised configuration set used by your algorithm for training

def trainCFG(pathForConfigFile, pathForCheckpointURL, trainingDatasetName, testDatasetName, classesNumber, device, outputDirectory):
    cfg = get_cfg()    # To get the default configuration of the model
    # The configuration we are using in our model .i.e. object detetcion
    cfg.merge_from_file(model_zoo.get_config_file(pathForConfigFile))
    # Giving the train dataset
    cfg.DATASETS.TRAIN = (trainingDatasetName,)
    cfg.DATASETS.TEST = ()  # we have no metrics implemented for this dataset
  #  cfg.DATASETS.TEST = (testDatasetName,)            # Giving the test dataset
    # The number of workers being run. The more it is, the more load on the system, the faster training is done.
    cfg.DATALOADER.NUM_WORKERS = 2
    # The weights that are being used in the model from the model zoo
    cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(pathForCheckpointURL)
    cfg.SOLVER.IMS_PER_BATCH = 2             # The number of images per batch
    cfg.SOLVER.BASE_LR = 0.00025             # The learning rate
    # The number of iterations with the training
    cfg.SOLVER.MAX_ITER = 1000
    # cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = 128         # Size of the images
    # Number of classes defined for the model to be trained
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = classesNumber
    cfg.SOLVER.STEPS = []       # To not reduce the learning rate in training
    cfg.MODEL.DEVICE = device    # The device on which the model is to be trained
    # The directory where custom object detetcion model would be saved
    cfg.OUTPUT_DIR = outputDirectory

    # Returning the customised configuration that we are using in this training model
    return cfg


# A function to load the image and show the prediction using the model created
# Parameters: imagePath --> file path to the image that is to be tested
#             predictor --> the configured predictor object that will do the prediction

def onImage(imagePath, predictor):
    img = cv.imread(imagePath)   # Load the image
    # Getting the output from the predictor
    outputs = predictor(img)
    # Passing the image to the visualiser
    visualizer = Visualizer(
        img[:, :, ::-1], metadata={}, scale=0.5, instance_mode=ColorMode.SEGMENTATION)
    # Drawing all the instances on the image
    vis = visualizer.draw_instance_predictions(outputs["instances"].to("cpu"))
    # Plot the figure
    plt.figure(figsize=(14, 10))
    plt.imshow(vis.get_image())
    plt.show()


# A function to load the video and show the prediction using the model created
# Parameters: videoPath --> file path to the video that is to be tested
#             predictor --> the configured predictor object that will do the prediction

def onVideo(videoPath, predictor):
    # Loading the video
    capture = cv.VideoCapture(videoPath)
    # Checking the video is loaded properly
    if (capture.isOpened() == False):
        print("Error in capturing the video..")
        return

    # Getting the frames
    (success, image) = capture.read()

    #  Repeat the loop until unless we quit
    while success:
        predictions = predictor(image)   # To do the predictions
        # Passing the image to the visualiser
        visualizer = Visualizer(
            image[:, :, ::-1], metadata={}, scale=0.5, instance_mode=ColorMode.SEGMENTATION)
        # Drawing all the instances on the image
        vis = visualizer.draw_instance_predictions(
            predictions["instances"].to("cpu"))

        # Showing the video using cv2
        cv.imshow("Result", vis.get_image()[:, :, ::-1])
        # A key press to quit the video
        key = cv.waitKey(1) & 0xFF

        if key == ord("q"):
            break

        (success, image) = capture.read()


# A function to allow the video input from the webcam of the laptop to
# show the prediction using the model created.
# Parameters: webcamNumber --> the number represening which webcam connected to the laptop is being used
#             predictor --> the configured predictor object that will do the prediction

def onWebcam(webcamNumber, predictor):

    # Taking the input from the webcam. The number 0 represents which camera to be used.
    webcam_input = cv.VideoCapture(webcamNumber)

    # An infinite loop that only breaks when you press "q".
    while True:
        # It returns two things: A Boolean value telling whether camera is functioning properly or not
        # Second it returns the frame
        isTrue, frame = webcam_input.read()
        image = frame
        predictions = predictor(image)   # To do the predictions

        # Passing the image to the visualiser
        visualizer = Visualizer(
            image[:, :, ::-1], metadata={}, scale=0.5, instance_mode=ColorMode.SEGMENTATION)
        # Drawing all the instances on the image
        vis = visualizer.draw_instance_predictions(
            predictions["instances"].to("cpu"))

        ret,buffer=cv.imencode('.jpg',vis.get_image()[:,:,::-1])
        frame=buffer.tobytes()

        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        # Showing the video using cv2
        # cv.imshow("Result_From_Webcam", vis.get_image()[:, :, ::-1])

        # A key press to quit the video
        # if cv.waitKey(1) == ord("q"):
        #     break

        # Takes parameter in seconds
        # time.sleep(10)


# A function to allow the video input from the RealSense depth camera to
# show the prediction using the model created.
# Parameters:    predictor --> the configured predictor object that will do the prediction

def onRealSense(predictor):

    # A counter for sending data and to avoid noise
    counter = 0

    # Initialising the DepthCamera.
    depthCamera = DepthCamera()

    # An infinite loop until unless q is pressed
    while True:
        # Getting the depthFrame and ColorFrame for further processing
        _, depthFrame, colorFrame = depthCamera.get_frame()
        # Doing prediction on the input given from the webcam
        image = colorFrame
        predictions = predictor(image)

        # Passing the image to the visualiser
        visualizer = Visualizer(
            image[:, :, ::-1], metadata={}, scale=0.5, instance_mode=ColorMode.SEGMENTATION)
        # Drawing all the instances on the image
        vis = visualizer.draw_instance_predictions(
            predictions["instances"].to("cpu"))

        # This line finds the number of classes and the x,y coordinates of the bounding boxes
        predictionBoxes = predictions["instances"].pred_boxes

        # Initialising this so that we are able to write in the image, the coordinates
        boxes = visualizer._convert_boxes(
            predictions["instances"].pred_boxes.to('cpu')).squeeze()

        # Coordinates that need to be sent
        coordinatesSent = []

        rightBoxFlag = False      # A flag just for demo/protoype to get the right box .i.e. 0

        # A loop to get the coordinates of all the bounding boxes
        for idx, coordinates in enumerate(predictionBoxes):

            print(
                "###########################################################################################")
            print("Box number is " + str(idx))
            # If it is box 0, then it is the right coordinate
            if idx == 0:
                rightBoxFlag = True

            # Getting the individual box
            box = list(predictionBoxes)[idx].detach().cpu().numpy()

            # Finding the x-y coordinates in a clockwise direction from the upper
            # left corner to the lower left corner. Also finds the width and center
            # of the bounding box
            x_top_left = box[0]
            y_top_left = box[1]
            x_bottom_right = box[2]
            y_bottom_right = box[3]
            x_center = (x_top_left + x_bottom_right)/2
            y_center = (y_top_left + y_bottom_right)/2
            width = abs(x_bottom_right - x_top_left)
            height = abs(y_bottom_right - y_top_left)
            x_top_right = x_top_left + width
            y_top_right = y_top_left
            x_bottom_left = x_top_left
            y_bottom_left = y_top_left + height
            # Prininting the coordinates on console/terminal for debugging
            # print("Top left x coordinate of the box is " + str(x_top_left))
            # print("Top left y coordinate of the box is " + str(y_top_left))
            # print("Top right x coordinate of the box is " + str(x_top_right))
            # print("Top right y coordinate of the box is " + str(y_top_right))
            # print("Bottom right x coordinate of the box is " + str(x_bottom_right))
            # print("Bottom right y coordinate of the box is " + str(y_bottom_right))
            # print("Bottom left x coordinate of the box is " + str(x_bottom_left))
            # print("Bottom left y coordinate of the box is " + str(y_bottom_left))
            # print("Width of the box is " + str(width))
            # print("Height of the box is " + str(height))
            # print("Center coordinates of the box are (x,y) = (" + str(x_center) + "," + str(y_center) + ").")

            # Getting the depth or distance from the camera of an object
            # X0,X1,X2,X4 are in clockwise direction from top left corner
            # Doing -1 to avoid an index out of the array array
            depthX0Y0 = depthFrame[int(y_top_left)-1, int(x_top_left)-1]
            depthX1Y1 = depthFrame[int(y_top_right)-1, int(x_top_right)-1]
            depthX2Y2 = depthFrame[int(
                y_bottom_right)-1, int(x_bottom_right)-1]
            depthX3Y3 = depthFrame[int(y_bottom_left)-1, int(x_bottom_left)-1]
            # Printing the distances
            # print("Depth at top left corner is " + str(depthX0Y0))
            # print("Depth at top right corner is " + str(depthX1Y1))
            # print("Depth at bottom right corner is " + str(depthX2Y2))
            # print("Depth at bottom left corner is " + str(depthX3Y3))
            # print("###########################################################################################")

            # coords = [x_top_left,y_top_left,depthX0Y0,x_top_right,y_top_right,depthX1Y1,x_bottom_right,y_bottom_right,depthX2Y2,x_bottom_left,y_bottom_left,depthX3Y3]
            # coordinatesSent.append(coords)
            # If the flag is true, send the coordinates
            if rightBoxFlag == True:
                coords = [x_top_left, y_top_left, depthX0Y0, x_top_right, y_top_right, depthX1Y1,
                          x_bottom_right, y_bottom_right, depthX2Y2, x_bottom_left, y_bottom_left, depthX3Y3]
                coordinatesSent = []
                coordinatesSent.extend(coords)
                break

            print('coordinates in the array after appending new object')
            print(coordinatesSent)

            # Writing the cooridnates on the image
            vis = visualizer.draw_text(
                f"{boxes[idx]}", (x_top_left, y_top_left))

        #  Printing the sizes just for debugging
        # print("Size of the image below *******#######")
        # print(image.shape)
        im = vis.get_image()[:, :, ::-1]
        # print(im.shape)

        # Showing the output from the camera using cv2
        cv.imshow("Result_From_RealSense", vis.get_image()[:, :, ::-1])

        # Sending coordinates
        # Commenting it down so that we can see what the camera is detecting
        if rightBoxFlag == True:
            print("Coordinates Sent")
            roboticarm.getmappedcoordinates(coordinatesSent, counter)
            counter += 1
        else:
            rightBoxFlag = False

        print("Final Coordinate array that we might need to send for cleaning")
        print(coordinatesSent)

        # A key press to quit the video
        if cv.waitKey(1) == ord("q"):
            break


#  A function just to test the coordinates
def test():
    roboticarm.getCoordinatesAndAngles()


# A function to allow the video input from the RealSense depth camera to
# show the prediction using the model created.
# Parameters:    predictor --> the configured predictor object that will do the prediction

def onRealSenseMultiple(predictor):

    # Initialising the DepthCamera.
    depthCamera = DepthCamera()

    # An infinite loop until unless q is pressed
    while True:
        # Getting the depthFrame and ColorFrame for further processing
        _, depthFrame, colorFrame = depthCamera.get_frame()
        # Doing prediction on the input given from the webcam
        image = colorFrame
        predictions = predictor(image)

        # Passing the image to the visualiser
        visualizer = Visualizer(
            image[:, :, ::-1], metadata={}, scale=0.5, instance_mode=ColorMode.SEGMENTATION)
        # Drawing all the instances on the image
        vis = visualizer.draw_instance_predictions(
            predictions["instances"].to("cpu"))

        # This line finds the number of classes and the x,y coordinates of the bounding boxes
        predictionBoxes = predictions["instances"].pred_boxes

        # Initialising this so that we are able to write in the image, the coordinates
        boxes = visualizer._convert_boxes(
            predictions["instances"].pred_boxes.to('cpu')).squeeze()

        # Coordinates that need to be sent
        coordinatesSent = []

        # A loop to get the coordinates of all the bounding boxes
        for idx, coordinates in enumerate(predictionBoxes):

            # Getting the individual box
            box = list(predictionBoxes)[idx].detach().cpu().numpy()

            # Finding the x-y coordinates in a clockwise direction from the upper
            # left corner to the lower left corner. Also finds the width and center
            # of the bounding box
            x_top_left = box[0]
            y_top_left = box[1]
            x_bottom_right = box[2]
            y_bottom_right = box[3]
            x_center = (x_top_left + x_bottom_right)/2
            y_center = (y_top_left + y_bottom_right)/2
            width = abs(x_bottom_right - x_top_left)
            height = abs(y_bottom_right - y_top_left)
            x_top_right = x_top_left + width
            y_top_right = y_top_left
            x_bottom_left = x_top_left
            y_bottom_left = y_top_left + height

            # Getting the depth or distance from the camera of an object
            # X0,X1,X2,X4 are in clockwise direction from top left corner
            # Doing -1 to avoid an index out of the array array
            depthX0Y0 = depthFrame[int(y_top_left)-1, int(x_top_left)-1]
            depthX1Y1 = depthFrame[int(y_top_right)-1, int(x_top_right)-1]
            depthX2Y2 = depthFrame[int(
                y_bottom_right)-1, int(x_bottom_right)-1]
            depthX3Y3 = depthFrame[int(y_bottom_left)-1, int(x_bottom_left)-1]

            coords = [x_top_left, y_top_left, depthX0Y0, x_top_right, y_top_right, depthX1Y1,
                      x_bottom_right, y_bottom_right, depthX2Y2, x_bottom_left, y_bottom_left, depthX3Y3]
            coordinatesSent.append(coords)

            print('coordinates in the array after appending new object')
            print(coordinatesSent)

            # Writing the cooridnates on the image
            vis = visualizer.draw_text(
                f"{boxes[idx]}", (x_top_left, y_top_left))

        im = vis.get_image()[:, :, ::-1]

        # Showing the output from the camera using cv2
        cv.imshow("Result_From_RealSense", vis.get_image()[:, :, ::-1])

        print("Final Coordinate array that we might need to send for cleaning")
        print(coordinatesSent)

        roboticarm.getmappedcoordinatesmultiple(coordinatesSent)
        # A key press to quit the video
        if cv.waitKey(1) == ord("q"):
            break


# A function to allow the video input from the RealSense depth camera to
# show the prediction using the model created.
# Parameters:    predictor --> the configured predictor object that will do the prediction

def onRealSenseViewer(predictor):

    # Initialising the DepthCamera.
    depthCamera = DepthCamera()

    # An infinite loop until unless q is pressed
    while True:
        # Getting the depthFrame and ColorFrame for further processing
        _, depthFrame, colorFrame = depthCamera.get_frame()
        # Doing prediction on the input given from the webcam
        image = colorFrame
        predictions = predictor(image)

        # Passing the image to the visualiser
        visualizer = Visualizer(
            image[:, :, ::-1], metadata={}, scale=0.5, instance_mode=ColorMode.SEGMENTATION)
        # Drawing all the instances on the image
        vis = visualizer.draw_instance_predictions(
            predictions["instances"].to("cpu"))

        # This line finds the number of classes and the x,y coordinates of the bounding boxes
        predictionBoxes = predictions["instances"].pred_boxes

        # Initialising this so that we are able to write in the image, the coordinates
        boxes = visualizer._convert_boxes(
            predictions["instances"].pred_boxes.to('cpu')).squeeze()

        # Coordinates that need to be sent
        coordinatesSent = []

        # A loop to get the coordinates of all the bounding boxes
        for idx, coordinates in enumerate(predictionBoxes):

            print(
                "###########################################################################################")
            print("Box number is " + str(idx))
            # If it is box 0, then it is the right coordinate

            # Getting the individual box
            box = list(predictionBoxes)[idx].detach().cpu().numpy()

            # Finding the x-y coordinates in a clockwise direction from the upper
            # left corner to the lower left corner. Also finds the width and center
            # of the bounding box
            x_top_left = box[0]
            y_top_left = box[1]
            x_bottom_right = box[2]
            y_bottom_right = box[3]
            x_center = (x_top_left + x_bottom_right)/2
            y_center = (y_top_left + y_bottom_right)/2
            width = abs(x_bottom_right - x_top_left)
            height = abs(y_bottom_right - y_top_left)
            x_top_right = x_top_left + width
            y_top_right = y_top_left
            x_bottom_left = x_top_left
            y_bottom_left = y_top_left + height

            # Getting the depth or distance from the camera of an object
            # X0,X1,X2,X4 are in clockwise direction from top left corner
            # Doing -1 to avoid an index out of the array array
            depthX0Y0 = depthFrame[int(y_top_left)-1, int(x_top_left)-1]
            depthX1Y1 = depthFrame[int(y_top_right)-1, int(x_top_right)-1]
            depthX2Y2 = depthFrame[int(
                y_bottom_right)-1, int(x_bottom_right)-1]
            depthX3Y3 = depthFrame[int(y_bottom_left)-1, int(x_bottom_left)-1]

            coords = [x_top_left, y_top_left, depthX0Y0, x_top_right, y_top_right, depthX1Y1,
                      x_bottom_right, y_bottom_right, depthX2Y2, x_bottom_left, y_bottom_left, depthX3Y3]
            coordinatesSent.append(coords)

            print('coordinates in the array after appending new object')
            print(coordinatesSent)

            # Writing the cooridnates on the image
            vis = visualizer.draw_text(
                f"{boxes[idx]}", (x_top_left, y_top_left))

        #  Printing the sizes just for debugging
        # print("Size of the image below *******#######")
        # print(image.shape)
        im = vis.get_image()[:, :, ::-1]
        # print(im.shape)

        # Showing the output from the camera using cv2
        cv.imshow("Result_From_RealSense", vis.get_image()[:, :, ::-1])

        print("Final Coordinate array that we might need to send for cleaning")
        print(coordinatesSent)

        # A key press to quit the video
        if cv.waitKey(1) == ord("q"):
            break

#  ********************* STAY SAFE, STAY HAPPY & KEEP SMILING **********************************
