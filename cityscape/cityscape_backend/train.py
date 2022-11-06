# Description: This file has a program that does the training for AIWindow Detetcion
# In this project, we are making use of Detectron2 developed by FAIR. 
# Credits to Detetcron2 developers:  
#                        authors =       Yuxin Wu and Alexander Kirillov and Francisco Massa and Wan-Yen Lo and Ross Girshick
#                        title  =       Detectron2
#                        url    =       https://github.com/facebookresearch/detectron2
#                        year   =       2019

# This code is being run Python 3.9.7 version, Macbook Pro, Chip Apple M1, MacOS Monterey, version 12.3.1

# To import necessary functions build in utils.py
from utiles import *

# import torch, torchvision

# Setting up logger after importing
from detectron2.utils.logger import setup_logger
setup_logger()
from detectron2.data.datasets import register_coco_instances     #To register the datasets
from detectron2.engine import DefaultTrainer        # A default trainer to continue with the training with the datasets


# Libraries to create and store necessary files
import os  
import pickle

# File path for the models that are to be used in the training.
# Link to different models: https://github.com/facebookresearch/detectron2/blob/main/MODEL_ZOO.md
# Just change the paths to try new models
pathForConfigFile = "COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml"
pathForCheckpointURL = "COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml"

# The directory where we want to save the custom model detection
outputDirectory = "./output/object_detection"

classesNumber = 1     # Only 1 class in our model .i.e. windows
device = "cpu"        # This is being run on macbook m1 pro hence we don't have GPU so we can't use cuda therefore we use cpu

trainingDatasetName = "WindowDetectionTrain"   # Dataset name given by us
# Necessary paths to annotation and images
trainingImagesPath = "./window_labeling_coco/images"
trainingAnnotationsPath = "./window_labeling_coco/annotations/instances_default.json"

testDatasetName = "WindowDetectionTest"      # Test dataset  name
# Paths necessary
testImagesPath = "./test"
testAnnotationsPath = "./test.json"

# Path where are pickle file would be saved
pathSaveCFG = "trained_cfg.pickle"

# **************************

# Regestring datasets for training
register_coco_instances(name = trainingDatasetName, metadata={}, json_file=trainingAnnotationsPath,image_root=trainingImagesPath)

# Register datasets for test
register_coco_instances(name = testDatasetName, metadata={}, json_file=testAnnotationsPath,image_root=testImagesPath)


# A function to just look into the images given as dataset and see annotations
# plottingSamples(datasetName=trainingDatasetName, number=2)

# The main function
def main():
    # Getting the necessary configuration that is used in the training
    cfg = trainCFG(pathForConfigFile,pathForCheckpointURL,trainingDatasetName, testDatasetName, classesNumber,device,outputDirectory)

    # Opening a file in pickle and saving the file in the necessary path
    with open(pathSaveCFG, 'wb') as f:
        pickle.dump(cfg,f,protocol=pickle.HIGHEST_PROTOCOL)
    
    # A directory where we want to save the model
    os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)
    print("We are done")
    trainer = DefaultTrainer(cfg)      # Loading the trainer.
    trainer.resume_or_load(resume=True)   #To resume traing from the previous checkpoints
    trainer.train()        # Starting to train the model

# Start of the program
if __name__ == '__main__':
    main()     # Running the main function 
    print("Training Done")    # Indicating training is done







#  ********************* STAY SAFE, STAY HAPPY & KEEP SMILING **********************************
