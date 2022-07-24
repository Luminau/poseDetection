import time
import cv2
import mss
import numpy as np
import pyautogui
import win32api
import win32con
import gc
import poseDetectionModule

# What key to press to quit and shutdown the auto-aim
aaQuitKey = "Q"
# Window title to go after and the height of the screenshots
videoGameWindowTitle = "Rainbow Six"
# Portion of screen to be captured (This forms a square/rectangle around the center of screen)
screenShotHeight = 300
screenShotWidth = 500
# For use in games that are 3rd person and character model interferes with the auto-aim
# EXAMPLE: Fortnite and New World
aaRightShift = 0
# Displays the Corrections per second in the terminal
cpsDisplay = True

# Initialize pose detection module
detector = poseDetectionModule.PoseDetection()
# Starting screenshot engine
selectedVideo = mss.mss()
# Used for forcing garbage collection
count = 0
sTime = time.time()
# Main loop Quit if Q is pressed
last_mid_coord = None
aimbot = False

while win32api.GetAsyncKeyState(ord(aaQuitKey)) == 0:
    # Selecting the correct game window
    try:
        videoGameWindows = pyautogui.getWindowsWithTitle(videoGameWindowTitle)
        videoGameWindow = videoGameWindows[0]
    except:
        print("The game window you are trying to select doesn't exist.")
        print("Check variable videoGameWindowTitle (typically on line 13")
        exit()

    # # Select that Window
    # videoGameWindow.activate()

    # Setting up the screen shots
    selectedArea = {"mon": 1, "top": videoGameWindow.top + (videoGameWindow.height - screenShotHeight) // 2,
                    "left": aaRightShift + ((videoGameWindow.left + videoGameWindow.right) // 2) - (
                                screenShotWidth // 2),
                    "width": screenShotWidth,
                    "height": screenShotHeight}

    # Getting screenshop, making into np.array and dropping alpha dimention.
    image = np.delete(np.array(selectedVideo.grab(selectedArea)), 3, axis=2)
    # image = selectedVideo.grab(selectedArea)
    # image = np.array(selectedVideo.grab(selectedArea))


    # # Detecting all the objects
    # results = model(npImg, size=320).pandas().xyxy[0]
    #
    # # Filtering out everything that isn't a person
    # filteredResults = results[(results['class'] == 0) & (results['confidence'] > confidence)]
    #
    # # Returns an array of trues/falses depending if it is in the center Autoaim box or not
    # cResults = ((filteredResults["xmin"] > cWidth - aaDetectionBox) & (
    #         filteredResults["xmax"] < cWidth + aaDetectionBox)) & \
    #            ((filteredResults["ymin"] > cHeight - aaDetectionBox) & (
    #                    filteredResults["ymax"] < cHeight + aaDetectionBox))

    # Removes persons that aren't in the center bounding box

    res = detector.detect_pose(image)
    lm_list = detector.find_point(image, res)
    if len(lm_list) != 0:
        print(lm_list[0])
    image = detector.draw_detected_pose(image, res)
    image = detector.draw_fps(image)


    # targets = filteredResults[cResults]
    #
    # # If there are people in the center bounding box
    # if len(targets) > 0:
    #     targets['current_mid_x'] = (targets['xmax'] + targets['xmin']) // 2
    #     targets['current_mid_y'] = (targets['ymax'] + targets['ymin']) // 2
    #     # Get the last persons mid coordinate if it exists
    #     if last_mid_coord:
    #         targets['last_mid_x'] = last_mid_coord[0]
    #         targets['last_mid_y'] = last_mid_coord[1]
    #         # Take distance between current person mid coordinate and last person mid coordinate
    #         targets['dist'] = np.linalg.norm(targets.iloc[:, [7, 8]].values - targets.iloc[:, [9, 10]], axis=1)
    #         targets.sort_values(by="dist", ascending=False)
    #
    #     # Take the first person that shows up in the dataframe (Recall that we sort based on Euclidean distance)
    #     xMid = round((targets.iloc[0].xmax + targets.iloc[0].xmin) / 2) + aaRightShift
    #     yMid = round((targets.iloc[0].ymax + targets.iloc[0].ymin) / 2)
    #
    #     box_height = targets.iloc[0].ymax - targets.iloc[0].ymin
    #     if headshot_mode:
    #         headshot_offset = box_height * 0.38
    #     else:
    #         headshot_offset = box_height * 0.2
    #     mouseMove = [xMid - cWidth, (yMid - headshot_offset) - cHeight]
    #     cv2.circle(npImg, (int(mouseMove[0] + xMid), int(mouseMove[1] + yMid - headshot_offset)), 3, (0, 0, 255))
    #
    #     # Moving the mouse
    #     if win32api.GetKeyState(0x14):
    #         win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int(mouseMove[0] * aaMovementAmp),
    #                              int(mouseMove[1] * aaMovementAmp), 0, 0)
    #     last_mid_coord = [xMid, yMid]
    # else:
    #     last_mid_coord = None
    #
    # # Loops over every item identified and draws a bounding box
    # for i in range(0, len(results)):
    #     (startX, startY, endX, endY) = int(results["xmin"][i]), int(results["ymin"][i]), int(
    #         results["xmax"][i]), int(results["ymax"][i])
    #
    #     confidence = results["confidence"][i]
    #
    #     idx = int(results["class"][i])
    #
    #     # draw the bounding box and label on the frame
    #     label = "{}: {:.2f}%".format(results["name"][i], confidence * 100)
    #     cv2.rectangle(npImg, (startX, startY), (endX, endY),
    #                   COLORS[idx], 2)
    #     y = startY - 15 if startY - 15 > 15 else startY + 15
    #     cv2.putText(npImg, label, (startX, y),
    #                 cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

    # Forced garbage cleanup every second
    count += 1
    if (time.time() - sTime) > 1:
        if cpsDisplay:
            print("CPS: {}".format(count))
        count = 0
        sTime = time.time()

        gc.collect(generation=0)

    # See visually what the Aimbot sees
    cv2.imshow('Live Feed', image)
    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        exit()
