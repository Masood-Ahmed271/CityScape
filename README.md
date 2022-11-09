---
Title: CityScape - (An ongoing project)
Author: Masood Ahmed
Email: 'masood20@connect.hku.hk' or 'mangimasood2000@gmail.com'
---

# CityScape

It is a project having both software and hardware components aiming to solve the problem of window cleaning and painting walls of high altitude skyscrapers. This project uses raspberry-pi to handle communication with the robotic hand while on the software side this project has a backend on python and it communicates with frontend on ReactJS via Flask.

__________________________________________________________________________________________________________________________

# The following details are for setting up robot and running it without dashboard facilities. (Version 1.0)

## Things required to run this program

Your should have python version greater than or equal to 3.9.7.
You should have numpy, matplotlib, opencv,cython,pycocotools, pickle pytorch with torchvision installed on your system with visual bacis C++ build tools.

*Note:* pip can also be replaced by pip3 given your systems configurations.

To install numpy:
```terminal/cmd
pip install numpy
```
To install matplotlib:
```terminal/cmd
pip install matplotlib
```
To install opencv:
```terminal/cmd
pip install opencv-python
```

To install cython:
```terminal/cmd
pip install Cython
```

To install pytorch and torchvision:
```terminal/cmd
pip install torch torchvision torchaudio
```
To install pickle:
```terminal/cmd
pip install pickle-mixin
```

To install visual bacis C++ build tools:
Install them through this link: https://visualstudio.microsoft.com/visual-cpp-build-tools/
While installing put a check on c++ build tools

To install pycocotools:
```terminal/cmd
pip install git+https://github.com/philferriere/cocoapi.git#egg=pycocotools&subdirectory=PythonAPI
```


After all this install detetcron2 on your system.
To check detetcron2 documentation, go to the following link: https://github.com/facebookresearch/detectron2
and 
https://detectron2.readthedocs.io/en/latest/

Use the following commands to install Detetcron2.
```terminal/cmd
git clone https://github.com/facebookresearch/detectron2.git

```
```terminal/cmd
python -m pip install -e detectron2
```

Now install the sdk for realsense camera and pyrealsense library if you want to use realsense with the experiment to get the coordinates and depth.
*For Windows!!*

Go to https://github.com/IntelRealSense/librealsense or directly to https://github.com/IntelRealSense/librealsense/blob/master/doc/distribution_windows.md and follow the
instructions to download sdk.

To check if the realsense sdk is insatlled properly,
In your terminal/cmd, run the following command
```terminal/cmd
realsense-viewer
```

It should show the gui and camera of input from the realsense camera.

*For MacOS!!*
You can go to the following link and install it following the instructions: https://github.com/IntelRealSense/librealsense/blob/master/doc/installation_osx.md
#### Note: Realsense sdk was showing errors on MacOS M1 Monetery version. Hoping, that by the time you guys are reading this, the problem is solved and Mlibrealsense has a good instructions of installing on MacOS.

Lastly, after installing sdk, run the following command on terminal/cmd
```terminal/cmd
pip install pyrealsense2
```

## To run the Code:
If you have cloned all the repository, you just need to go to the terminal/cmd and run the following command where you have stored the codes.

```terminal/cmd
python window_detection.py
```

You can retrain the model and run it as well.
For retraining, run the following command:
```terminal/cmd
python train.py
```

You should be good to go :) 


for saving purpose
C:\Users\Clearbot\AppData\Local\Programs\Python\Python37\Scripts\


## To run the Code for the robotic-hand along with AI-Camera:

Open 2 terminals and go to the right directory.
In one terminal write the following command where the ipaddress can be found using ifconfig on the terminal (Note -> Both the roboic hand and Machine running the code should be connected to the same wifi.):

```terminal/cmd
ssh ubuntu@'ipaddress'
./run.sh
```

Password for the ssh into the mahcine is 'mycobotpi'

In the second terminal write the following command:

```terminal/cmd
python window_detection.py
```


# Details for Dashboard Setup. (Version 1.0 (Will be updated later))

## Dependencies Required:

To install dependencies for Frontend:
```terminal/cmd
npm install antd
npm install react-router-dom
```

### Important Thing:

Always run after making changes:

```terminal/cmd
npm run build
```
in the react frontend folder.

Then run the app in the backend by:
```terminal/cmd
    python3 App.py
```
