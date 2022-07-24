import time
import cv2
import mss
import numpy as np
import pyautogui
import win32api
import win32con
import gc
import poseDetectionModule


class GetWindowImage():
    def __init__(self, aaQuitKey="M", videoGameWindowTitle="Rainbow Six", screenShotHeight=300, screenShotWidth=500,
                 aaRightShift=0, cpsDisplay=True):
        self.aaQuitKey = aaQuitKey
        self.videoGameWindowTitle = videoGameWindowTitle
        self.screenShotHeight = screenShotHeight
        self.screenShotWidth = screenShotWidth
        self.aaRightShift = aaRightShift
        self.cpsDisplay = cpsDisplay
        # Starting screenshot engine
        self.selectedVideo = mss.mss()
        # Used for forcing garbage collection
        self.count = 0
        self.sTime = time.time()
        # Main loop Quit if Q is pressed
        self.last_mid_coord = None
        self.aimbot = False

    def getSelectedArea(self,screenShotHeight=300, screenShotWidth=500):
        self.screenShotHeight = screenShotHeight
        self.screenShotWidth = screenShotWidth
        # Selecting the correct game window
        try:
            videoGameWindows = pyautogui.getWindowsWithTitle(self.videoGameWindowTitle)
            videoGameWindow = videoGameWindows[0]
        except:
            print("The game window you are trying to select doesn't exist.")
            print("Check variable videoGameWindowTitle (typically on line 13")
            exit()

        # Setting up the screen shots
        self.selectedArea = {"mon": 1, "top": videoGameWindow.top + (videoGameWindow.height - screenShotHeight) // 2,
                        "left": self.aaRightShift + ((videoGameWindow.left + videoGameWindow.right) // 2) - (
                                screenShotWidth // 2),
                        "width": self.screenShotWidth,
                        "height": self.screenShotHeight}
        return self.selectedArea


    def getWindowImage(self,screenShotHeight=300, screenShotWidth=500):
        self.screenShotHeight = screenShotHeight
        self.screenShotWidth = screenShotWidth
        # Selecting the correct game window
        try:
            videoGameWindows = pyautogui.getWindowsWithTitle(self.videoGameWindowTitle)
            videoGameWindow = videoGameWindows[0]
        except:
            print("The game window you are trying to select doesn't exist.")
            print("Check variable videoGameWindowTitle (typically on line 13")
            exit()

        # Setting up the screen shots
        selectedArea = {"mon": 1, "top": videoGameWindow.top + (videoGameWindow.height - screenShotHeight) // 2,
                        "left": self.aaRightShift + ((videoGameWindow.left + videoGameWindow.right) // 2) - (
                                screenShotWidth // 2),
                        "width": self.screenShotWidth,
                        "height": self.screenShotHeight}
        # Getting screenshop, making into np.array and dropping alpha dimention.
        image = np.delete(np.array(self.selectedVideo.grab(selectedArea)), 3, axis=2)
        return image

    def getselectedWindowImage(self,screenShotHeight=300, screenShotWidth=500):
        # Getting screenshop, making into np.array and dropping alpha dimention.
        image = np.delete(np.array(self.selectedVideo.grab(self.selectedArea)), 3, axis=2)
        return image

    def showImage(self, image):
        # Forced garbage cleanup every second
        self.count += 1
        if (time.time() - self.sTime) > 1:
            if self.cpsDisplay:
                print("CPS: {}".format(self.count))
            self.count = 0
            self.sTime = time.time()

            gc.collect(generation=0)

        # See visually what the Aimbot sees
        cv2.imshow('Live Feed', image)
        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            exit()


def main():
    wimg = GetWindowImage(videoGameWindowTitle="Anaconda P")
    while True:
        img = wimg.getWindowImage()
        wimg.showImage(img)

if __name__ == "__main__":
    main()