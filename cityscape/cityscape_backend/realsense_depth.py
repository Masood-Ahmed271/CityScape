# Description: A file that contains essential functions/methods and objects that can be used to get the depth and
# And image from the realsense2 camera.


import pyrealsense2 as rs       # Library to interact with realsense camera
import numpy as np              # Numpy for manipulating an array

class DepthCamera:

    def __init__(self):
        #Configure depth and color schemes
        self.pipeline = rs.pipeline()      # Creating a pipeline
        config = rs.config()        # Providing different resoltuions for color and depth streams

        #Getting device product line for setting a supporting resolution
        pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
        pipeline_profile = config.resolve(pipeline_wrapper)
        device  = pipeline_profile.get_device()
        device_product_line = str(device.get_info(rs.camera_info.product_line))

        # A condition to check if the camera is connected properly
        foundCamera = False
        for s in device.sensors:
            if s.get_info(rs.camera_info.name) == 'RGB Camera':
                foundCamera = True
                break
        if not foundCamera:
            print("We don't have a realsense camera attached for demo :( :(")
            exit(0)


        config.enable_stream(rs.stream.depth,640,480,rs.format.z16,30)

        if device_product_line == 'L500':
            config.enable_stream(rs.stream.color,960,540,rs.format.bgr8,30)
        else:
            config.enable_stream(rs.stream.color,640,480,rs.format.bgr8,30)

        #starting streaming
        self.pipeline.start(config)

    # A method that gets the depth and colored frame from the realsense camera and sends the frame/Image 
    # to for future processing
    def get_frame(self):

        frames = self.pipeline.wait_for_frames()     # Getting the frames
        depth_frame = frames.get_depth_frame()       # Getting the depth frame
        color_frame = frames.get_color_frame()       # Getting the colored frame

        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        if not depth_frame or not color_frame:
            return False, None, None
        return True, depth_image, color_image

    #  To release the pipeline for future processing
    def release(self):
        self.pipeline.stop()







#  ********************* STAY SAFE, STAY HAPPY & KEEP SMILING **********************************

