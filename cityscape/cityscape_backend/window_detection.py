# Description: A program that tests the trained model on some pictures and videos.
# In this project, we are making use of Detectron2 developed by FAIR. 
# Credits to Detetcron2 developers:  
#                        authors =      Yuxin Wu and Alexander Kirillov and Francisco Massa and Wan-Yen Lo and Ross Girshick
#                        title  =       Detectron2
#                        url    =       https://github.com/facebookresearch/detectron2
#                        year   =       2019

# This code is being run Python 3.9.7 version, Macbook Pro, Chip Apple M1, MacOS Monterey, version 12.3.1

# Importing everything from the utils.py to be used in this testing program
from utiles import *

from detectron2.engine import DefaultPredictor      # To use the predictor of detetctron2
# To deal with opeinig of the files
import os
import pickle

#Importing Pyrealsense Processing libraries
import pyrealsense2
from realsense_depth import *

# Getting the trained file
pathSaveCFG = "trained_cfg.pickle"

# Opeining the file for reading and loading it into the configuration file
with open(pathSaveCFG, 'rb') as f:
    cfg = pickle.load(f)

# To load the  wights that we had defined
cfg.MODEL.WEIGHTS = os.path.join(cfg.OUTPUT_DIR,"model_final.pth")
# Threshold for the detetcion
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5

# Passing the configuration to our predictor to predict
predictor = DefaultPredictor(cfg)

imagePath = "../AI_Model_MyCobot/test/Skyscrapper6.jpg"  # Path from the test images to test an image
videoPath = "../AI_Model_MyCobot/test/Testing_Window_Detetcion_Algo.mp4"   # Path from the test video to test an image

# To use the predictor on an image
# onImage(imagePath, predictor)

# To use the predictor on a video
# onVideo(videoPath, predictor)

# To use the predictor on webCam input
# As we would only be using one camera, so it's number would be webcamNumber: 0
# onWebcam(0,predictor)

# To use the predictor on Realsense input
# onRealSense(predictor)

# To use the predictor on Realsense input for multiple windows
onRealSenseMultiple(predictor)

# onRealSenseViewer(predictor)

# We are calling test() just to get the desired coordinates or where the robotic arm is .i.e. angles and coordinates
# print('Testing function')
# test()

# [89.0, -56.632934265136726, 349.33276824951173, 50.16086669921873, 349.33276824951173, 50.16086669921873, 272.1499214172363, -56.632934265136726, 272.1499214172363]





#  ********************* STAY SAFE, STAY HAPPY & KEEP SMILING **********************************