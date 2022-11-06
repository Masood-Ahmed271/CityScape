from telnetlib import PRAGMA_HEARTBEAT
from time import sleep
from tkinter import SW
from pymycobot import MyCobotSocket
import time
mc = MyCobotSocket("192.168.166.103", 9000)
mc.connect()

# A function that recieves coordinates from the realsense and maps them
# onto the mycobot coordinate system and asks the my cobot to go that coordinate
# Parameters:    coords --> Send a list of coordinates .i.e. [x1,y1,z1,x2,y2,z2,x3,y3,z3,x4,y4,z4]
#                counter -->  A counter to let us avoid initial image which is out of coordinates
# Returns:       Nothing


def getmappedcoordinates(coords, counter):

    print("In mapping function")

    # if counter's value is 0, hence initial image is noise and do not proceed
    if counter != 0:
        print("Leaviing the mapping function because it has some kind of noise")
        return

    # X is the x axis coordinates of realsense
    # y is the y axis coordinates of realsense
    # z is the depth

    # Creating a matrix called transformation matrix (has been changed because of new mapping)
    #     0.87       0    -320
    #     0       -0.93    450

    print('Starting coords sent')
    mc.send_angles([87.45, 116.98, -153.98, 41.57, 5.8, 0.08], 20)
    time.sleep(10)

    # ********************* Putting the robot at zero position (Initialisig) *************
    print('Straightening Up')
    mc.send_angles([0, 0, 0, 0,  0, 0], 20)
    time.sleep(5)
    # ********************* Putting the robot at zero position *************

    # Creating an Array to be sent to the sweeping function
    #  In the SweepArray we just want one depth point because surface would be flat (Assumption)
    depthCounter = 0
    # Array = [depth, ULCornerX, ULCornerY, URCornerX, URCornerY, LRCornerX, LRCornerY, LLCornerX,LLCornerY]
    SweepArray = []

    # Depth given by realsense is in mm
    # There is a loop because some of coordinates sent by the realsene (depth) seem to be 0
    for j in range(4):
        print("Loop running time: --> " + str(j))
        print("coords in getmapped coordinates")
        print(coords)
        print("STARTED MAPPING")
        # # Original Mapping coordinates  (Old Mapping Functions)
        # x = float(coords[(j*2+j)])*0.87 - 320
        # y = float(coords[(j*2+j)+1])*(-0.95) + 455

        # Testing new mapping functions
        print("The x-coordinate being converted to x for robot is " +
              str(coords[(j*2+j)]) + " at loop " + str(j))
        print("The y-coordinate being converted to y for robot is " +
              str(coords[(j*2+j) + 1]) + " at loop " + str(j))
        x = float(coords[(j*2+j)])*0.87 - 350
        y = float(coords[(j*2+j)+1])*(-0.95) + 520
        print("The converted x-coordinate is " + str(x) + " at loop " + str(j))
        print("The converted y-coordinate is " + str(y) + " at loop " + str(j))

        for i in range(4):
            if coords[2+(i*3)] != 0:
                print("Found Depth Coordiante")
                # Y on mycobot coords originally it was just 6
                mycobotDepth = float(coords[2+(i*3)])//(6.5)
                if depthCounter == 0:
                    SweepArray.append(mycobotDepth)
                    depthCounter += 1
                print("X --> " + str(x))
                print("depth --> " + str(mycobotDepth))
                print("y --> " + str(y))
                print("Corner: --> " + str(j))
                break
        SweepArray.append(x)
        SweepArray.append(y)

    #  Calling Sweep Function
    print('Called Sweep Function')
    print(SweepArray)
    sweepingWindow(SweepArray, 2, 10)

    # Getting back
    depthCounter = 0
    mc.send_angles([87.45, 116.98, -153.98, 41.57, 5.8, 0.08], 20)
    time.sleep(10)
    print("Leaving Function")
    return


def resetpos():
    print("I am inside the robot")
    res = mc.get_coords()
    print(res)
    print("I am here")
    mc.send_coords([100.8, 198.4, 2005.8, -85.52, 12.01, 6.22], 50, 1)
    time.sleep(10)
    # mc.send_angles([0,-75,75,0,0,0],20)

    # ********************* Putting the robot at zero position *************
    mc.send_angles([0, 0, 0, 0,  0, 0], 20)
    time.sleep(10)
    # ********************* Putting the robot at zero position *************

    # mc.release_all_servos()
    return 0


# A function that sweeps and cleans the window
# Parameters:    SweepArray --> Send a list of coordinates .i.e. [depth, ULCornerX, ULCornerY, URCornerX, URCornerY, LRCornerX, LRCornerY, LLCornerX,LLCornerY]
#                NoOfSweeps -->  The number of times you want the arm to move left and right at a single heigh
#                DepthStep --> The distance that you want the arm to go down after perfoming sweeps
# Returns:       Nothing

def sweepingWindow(SweepArray, NoOfSweeps, DepthStep):
    print("Inside the sweeping array")
    print(SweepArray)
    belowToReach = SweepArray[6]
    belowOriginal = SweepArray[2]
    while (belowOriginal > belowToReach):
        for i in range(NoOfSweeps):
            mc.send_coords([SweepArray[1], SweepArray[0],
                           belowOriginal, -85.99, 35.78, 8.32], 20, 0)
            time.sleep(3)
            mc.send_coords([SweepArray[3], SweepArray[0],
                           belowOriginal, -85.99, 35.78, 8.32], 20, 0)
            time.sleep(3)

        belowOriginal -= DepthStep
    return


def sweep(topleftcorner=[], bottomrightcorner=[]):

    res = mc.get_coords()
    print(res)
    mc.send_coords([-31.9, 127.6, 285.5, 80.1, 89.1, 80.1], 20, 1)
    time.sleep(5)
    i = 10  # horizontal offset
    j = 10  # vertical offset
    k = 30  # backward jump during sweep
    topreset = topleftcorner[2]
    bottomreset = bottomrightcorner[2]
    tempcord = topleftcorner
    mc.send_coords(tempcord, 80, 1)
    time.sleep(2)
    tempcord[0] = tempcord[0]-i
    while tempcord[0] < bottomrightcorner[0]:
        tempcord[0] = round(tempcord[0]+i)
        tempcord[2] = topreset
        print(tempcord)
        while tempcord[2] > bottomreset:
            tempcord[2] = tempcord[2]-j
            mc.send_coords(tempcord, 80, 1)
            print(tempcord)
            time.sleep(0.1)
        tempcord[1] = tempcord[1]-k
        # another step back so that the gripper does not touch during upward reset motion
        while tempcord[2] < topreset:
            tempcord[2] = tempcord[2]+j
            mc.send_coords(tempcord, 80, 1)
            print(tempcord)
            time.sleep(0.1)
        tempcord[1] = tempcord[1]+k
        time.sleep(0.1)
    mc.send_coords([-31.9, 127.6, 285.5, 80.1, 89.1, 80.1], 20, 1)
    time.sleep(5)
    mc.release_all_servos()
    # print("Coordinates Sent")
    return 0


# A function that recieves nothing and just gives the coordinates and the angles of the robotic arm
# Returns:       Nothing
def getCoordinatesAndAngles():
    print('Desired coords needed below')
    print(mc.get_coords())
    print("Gotten Coordinates")
    print('Starting coords sent')
    mc.send_angles([87.45, 116.98, -153.98, 41.57, 5.8, 0.08], 20)
    time.sleep(10)
    mc.send_angles([0, 0, 0, 0,  0, 0], 20)
    time.sleep(10)
    print(mc.get_coords())
    time.sleep(5)
    #               x       depth     y
    # mc.send_coords([36.25, 178.4, 370.5, -90.12, -3.28, 10.99],50,1)
    # -85.99, 35.78, 8.32 20, 0
    # mc.send_coords([33.25, 190.4, 365.0, -83.12, -45.43, 6.99],50,1)
    # mc.send_coords([33.25, 190.4, 360.0, -85.99, 35.78, 8.32],20,0)
    mc.send_coords([-56.6, 178.4, 349.33, -85.99, 35.78, 8.32], 20, 0)
    time.sleep(10)
    mc.send_angles([0, 0, 0, 0,  0, 0], 20)
    time.sleep(10)
    print('Starting coords sent')
    mc.send_angles([87.45, 116.98, -153.98, 41.57, 5.8, 0.08], 20)
    time.sleep(10)
    mc.release_all_servos()
    print('Desired Angles Needed')
    print(mc.get_angles())
    return


def testing():
    print("Working.....................")


# old equations: -> x = x'(0.87) - 350  & y = y'(-0.95) + 520
# Adding new equations: -> x = x'(0.87) - 290  & y = y'(-0.95) + 490
def getmappedcoordinatesmultiple(finalArray):

    print("Inside multiple window detector")

    # X is the x axis coordinates of realsense
    # y is the y axis coordinates of realsense
    # z is the depth

    # Creating a matrix called transformation matrix (has been changed because of new mapping)
    #     0.87       0    -320
    #     0       -0.93    450

    # Checking the range of given coordinates

    print("The array sent to the function to find range")
    coords = []

    for obj in finalArray:
        shouldAppend = True
        print("on index 0 the value is " + str(obj[0]))
        print("on index 1 the value is " + str(obj[1]))
        # print("on index 2 the value is " + str(obj[2]))
        print("on index 3 the value is " + str(obj[3]))
        print("on index 4 the value is " + str(obj[4]))
        # print("on index 5 the value is " + str(obj[5]))
        print("on index 6 the value is " + str(obj[6]))
        print("on index 7 the value is " + str(obj[7]))
        # print("on index 8 the value is " + str(obj[8]))
        print("on index 9 the value is " + str(obj[9]))
        print("on index 10 the value is " + str(obj[10]))
        rangex0 = float(obj[0])*0.87 - 290
        rangey1 = float(obj[1])*(-0.95) + 495
        rangex3 = float(obj[3])*0.87 - 290
        rangey4 = float(obj[4])*(-0.95) + 495
        rangex6 = float(obj[6])*0.87 - 290
        rangey7 = float(obj[7])*(-0.95) + 495
        rangex9 = float(obj[9])*0.87 - 290
        rangey10 = float(obj[10])*(-0.95) + 495
        print("rangex0 is " + str(rangex0))
        print("rangey1 is " + str(rangey1))
        print("rangex3 is " + str(rangex3))
        print("rangey4 is " + str(rangey4))
        print("rangex6 is " + str(rangex6))
        print("rangey7 is " + str(rangey7))
        print("rangex9 is " + str(rangex9))
        print("rangey10 is " + str(rangey10))
        if (rangex0 < -130 or rangex9 < -130):
            shouldAppend = False
        elif (rangex3 > 102 or rangex6 > 102):
            shouldAppend = False
        elif (rangey1 > 360 or rangey4 > 360):
            shouldAppend = False
        elif (rangey7 < 35 or rangey10 < 35):
            shouldAppend = False

        if shouldAppend != False:
            coords.append(obj)
            print("Final array with coords added")
            print(coords)

    print('Starting coords sent')
    mc.send_angles([87.45, 116.98, -153.98, 41.57, 5.8, 0.08], 20)
    time.sleep(10)

    # ********************* Putting the robot at zero position (Initialisig) *************
    print('Straightening Up')
    mc.send_angles([0, 0, 0, 0,  0, 0], 20)
    time.sleep(5)
    # ********************* Putting the robot at zero position *************

    # Creating an Array to be sent to the sweeping function
    #  In the SweepArray we just want one depth point because surface would be flat (Assumption)
    depthCounter = 0
    # Array = [depth, ULCornerX, ULCornerY, URCornerX, URCornerY, LRCornerX, LRCornerY, LLCornerX,LLCornerY]
    SweepArray = []

    # Depth given by realsense is in mm
    # There is a loop because some of coordinates sent by the realsene (depth) seem to be 0
    for object in range(len(coords)):
        print("Inside the first detected window")
        depthCounter = 0
        SweepArray = []
        for j in range(4):
            print("Loop running time: --> " + str(j))
            print("coords in getmapped coordinates")
            print(coords[object])
            print("STARTED MAPPING")
            # # Original Mapping coordinates  (Old Mapping Functions)
            # x = float(coords[(j*2+j)])*0.87 - 320
            # y = float(coords[(j*2+j)+1])*(-0.95) + 455

            # Testing new mapping functions
            print("The x-coordinate being converted to x for robot is " +
                  str(coords[object][(j*2+j)]) + " at loop " + str(j))
            print("The y-coordinate being converted to y for robot is " +
                  str(coords[object][(j*2+j) + 1]) + " at loop " + str(j))
            x = float(coords[object][(j*2+j)])*0.87 - 290
            y = float(coords[object][(j*2+j)+1])*(-0.95) + 495
            print("The converted x-coordinate is " +
                  str(x) + " at loop " + str(j))
            print("The converted y-coordinate is " +
                  str(y) + " at loop " + str(j))

            for i in range(4):
                if coords[object][2+(i*3)] != 0:
                    print("Found Depth Coordiante")
                    # Y on mycobot coords originally it was just 6
                    mycobotDepth = float(coords[object][2+(i*3)])//(3)
                    if depthCounter == 0:
                        SweepArray.append(mycobotDepth)
                        depthCounter += 1
                    print("X --> " + str(x))
                    print("depth --> " + str(mycobotDepth))
                    print("y --> " + str(y))
                    print("Corner: --> " + str(j))
                    break

            SweepArray.append(x)
            SweepArray.append(y)

        #  Calling Sweep Function
        print('Called Sweep Function')
        print(SweepArray)
        sweepingWindow(SweepArray, 1, 10)

        # ********************* Putting the robot at zero position (Initialisig) *************
        print('Straightening Up')
        mc.send_angles([0, 0, 0, 0,  0, 0], 20)
        time.sleep(5)
        # ********************* Putting the robot at zero position *************

    # Getting back
    depthCounter = 0
    mc.send_angles([87.45, 116.98, -153.98, 41.57, 5.8, 0.08], 20)
    time.sleep(10)
    print("Leaving Function")
    return


def viewer():
    pass
