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

from detectron2.utils.visualizer import Visualizer, ColorMode

#Importing Pyrealsense Processing libraries
# import pyrealsense2
# from realsense_depth import *

import flask
from flask import Flask

import cv2

app = Flask(__name__)
#app.config["DEBUG"] = True # Enable debug mode to enable hot-reloader.
# camera=cv2.VideoCapture(0)

def onWebcam(webcamNumber, predictor):

    print("I am here")
    # Taking the input from the webcam. The number 0 represents which camera to be used.
    webcam_input = cv2.VideoCapture(webcamNumber)

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

    # To use the predictor on Realsense input
    # onRealSense(predictor)

    # To use the predictor on Realsense input for multiple windows
    # onRealSenseMultiple(predictor)

    # onRealSenseViewer(predictor)

def generate_frames():
    while True:
            
        ## read the camera frame
        success,frame=camera.read()
        if not success:
            break
        else:
            ret,buffer=cv2.imencode('.jpg',frame)
            frame=buffer.tobytes()

        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return flask.render_template("index.html", token="cityscape testing")

# @app.route('/video')
# def video():
#     return flask.Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video')
def video():
    return flask.Response(runOperations(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=5002)