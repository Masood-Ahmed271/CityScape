# Description: A program that tests the trained model on some pictures and videos.
# In this project, we are making use of Detectron2 developed by FAIR. 
# Credits to Detetcron2 developers:  
#                        authors =      Yuxin Wu and Alexander Kirillov and Francisco Massa and Wan-Yen Lo and Ross Girshick
#                        title  =       Detectron2
#                        url    =       https://github.com/facebookresearch/detectron2
#                        year   =       2019

# This code is being run Python 3.9.7 version, Macbook Pro, Chip Apple M1, MacOS Monterey, version 12.3.1

# Importing everything from the utils.py to be used in this testing program
# from utiles import *

from detectron2.engine import DefaultPredictor      # To use the predictor of detetctron2
# To deal with opening of the files
import os
import pickle

# for opening ssh connection
import paramiko


from detectron2.utils.visualizer import Visualizer, ColorMode

#Importing Pyrealsense Processing libraries
import pyrealsense2
from realsense_depth import *
import roboticarm

import flask
from flask import Flask

import cv2

app = Flask(__name__)
#app.config["DEBUG"] = True # Enable debug mode to enable hot-reloader.

def runOperations():
    # Getting the trained file
    pathSaveCFG = "./trained_cfg.pickle"

    # Opeining the file for reading and loading it into the configuration file
    with open(pathSaveCFG, 'rb') as f:
        cfg = pickle.load(f)

    # To load the  wights that we had defined
    cfg.MODEL.WEIGHTS = os.path.join(cfg.OUTPUT_DIR,"model_final.pth")

    # Threshold for the detetcion
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5

    # Passing the configuration to our predictor to predict
    predictor = DefaultPredictor(cfg)


    # To use the predictor on webCam input
    # As we would only be using one camera, so it's number would be webcamNumber: 0
    # onWebcam(0,predictor)
    webcam_input = cv2.VideoCapture(0)

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

        ret,buffer=cv2.imencode('.jpg',vis.get_image()[:,:,::-1])
        frame=buffer.tobytes()

        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def onRealSenseWithoutSendingCoordinates():

    # Getting the trained file
    pathSaveCFG = "./trained_cfg.pickle"

    # Opeining the file for reading and loading it into the configuration file
    with open(pathSaveCFG, 'rb') as f:
        cfg = pickle.load(f)

    # To load the  wights that we had defined
    cfg.MODEL.WEIGHTS = os.path.join(cfg.OUTPUT_DIR,"model_final.pth")

    # Threshold for the detetcion
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5

    # Passing the configuration to our predictor to predict
    predictor = DefaultPredictor(cfg)

    # initializing the depth camera
    depthCamera = DepthCamera()

    # An infinite loop 
    while True:
        
        # Getting depth frame anc color frame for further processing
        _, depthFrame, colorFrame = depthCamera.get_frame()
        # Doing prediction on the input given from the RealSense camera
        image = colorFrame
        predictions = predictor(image)

        # passing the image to the visualiser
        visualizer = Visualizer(
            image[:,:,::-1], metadata={}, scale=0.5, instance_mode=ColorMode.SEGMENTATION)
        
        # Drawing all instances on the image

        vis = visualizer.draw_instance_predictions(
            predictions["instances"].to("cpu"))

        ret,buffer=cv2.imencode('.jpg',vis.get_image()[:,:,::-1])
        frame=buffer.tobytes()

        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def onRealSenseMultiple():
    # Getting the trained file
    pathSaveCFG = "./trained_cfg.pickle"

    # Opeining the file for reading and loading it into the configuration file
    with open(pathSaveCFG, 'rb') as f:
        cfg = pickle.load(f)

    # To load the  wights that we had defined
    cfg.MODEL.WEIGHTS = os.path.join(cfg.OUTPUT_DIR,"model_final.pth")

    # Threshold for the detetcion
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5

    # Passing the configuration to our predictor to predict
    predictor = DefaultPredictor(cfg)

    # initializing the depth camera
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
        
        ret,buffer=cv2.imencode('.jpg',vis.get_image()[:,:,::-1])
        frame=buffer.tobytes()

        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

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
            # vis = visualizer.draw_text(
            #     f"{boxes[idx]}", (x_top_left, y_top_left))
            


        print("Final Coordinate array that we might need to send for cleaning")
        print(coordinatesSent)

        roboticarm.getmappedcoordinatesmultiple(coordinatesSent)

def onRealSense():
    # Getting the trained file
    pathSaveCFG = "./trained_cfg.pickle"

    # Opeining the file for reading and loading it into the configuration file
    with open(pathSaveCFG, 'rb') as f:
        cfg = pickle.load(f)

    # To load the  wights that we had defined
    cfg.MODEL.WEIGHTS = os.path.join(cfg.OUTPUT_DIR,"model_final.pth")

    # Threshold for the detetcion
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5

    # Passing the configuration to our predictor to predict
    predictor = DefaultPredictor(cfg)

    # initializing the depth camera
    depthCamera = DepthCamera()

    # A counter for sending data and to avoid noise
    counter = 0

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

        ret,buffer=cv2.imencode('.jpg',vis.get_image()[:,:,::-1])
        frame=buffer.tobytes()

        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        # This line finds the number of classes and the x,y coordinates of the bounding boxes
        predictionBoxes = predictions["instances"].pred_boxes

        # Initializing this so that we are able to write in the image, the coordinates
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

@app.route('/')
def index():
    return flask.render_template("index.html", token="cityscape testing")

@app.route('/video')
def video():
    return flask.Response(runOperations(),mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/video')
# def video():
#     return flask.Response(onRealSense(),mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/video')
# def video():
#     return flask.Response(onRealSenseMultiple(),mimetype='multipart/x-mixed-replace; boundary=frame')
    
# @app.route('/video')
# def video():
#     return flask.Response(onRealSenseWithoutSendingCoordinates()(),mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/up')
def up():
    roboticarm.movement('up')
    return {"Status" : "up"}

@app.route('/down')
def down():
    roboticarm.movement('down')
    return {"Status" : "down"}

@app.route('/left')
def left():
    roboticarm.movement('left')
    return {"Status" : "left"}

@app.route('/right')
def right():
    roboticarm.movement('right')
    return {"Status" : "right"}

@app.route('/depthin')
def depthIn():
    roboticarm.movement('in')
    return {"Status" : "depthin"}

@app.route('/depthout')
def depthOut():
    roboticarm.movement('out')
    return {"Status" : "depthout"}

@app.route('/ssh_connection')
def sshConnection():
    ip = None
    username = 'ubuntu'
    connection_password = 'mycobotpi'
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username=username, password=connection_password)
    session = client.get_transport().open_session()
    if session.active:
        session.exec_command('./run.sh')
        print(session.recv(1024))
    client.close()

if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=5002)