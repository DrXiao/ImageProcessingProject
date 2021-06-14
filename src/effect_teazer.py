import numpy as np
import cv2
import imutils
import time
from ffpyplayer.player import MediaPlayer
from PIL import Image
video_path = 'movie/seal.mp4'

##

##


def preprocess(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 灰階
    ret, img = cv2.threshold(img, 165, 255, cv2.THRESH_BINARY)  # 門檻
    # fgmask_diff = cv2.cvtColor(fgmask_diff, cv2.COLOR_GRAY2BGR)
    return img


lastFrame = None



def img_process(orgimg, img):

    global lastFrame
    frame_preprocess = preprocess(img)
    if(lastFrame is None):
        lastFrame = frame_preprocess
    fgmask_diff = cv2.absdiff(frame_preprocess, lastFrame)
    lastFrame = frame_preprocess
    fgmask_diff = cv2.cvtColor(fgmask_diff, cv2.COLOR_GRAY2BGR)
    # dst=cv2.addWeighted(orgimg,0.7,fgmask_diff,0.3,0)
    dst = cv2.bitwise_not(orgimg,fgmask_diff)
    # dst = cv2.addWeighted(orgimg,0.7,fgmask_diff,0.1,0)
    # dst = cv2.bitwise_not(fgmask_diff,orgimg)
    # dst = cv2.addWeighted(orgimg,0.9,dst,0.1,0)  
    # dst = cv2.bitwise_not(dst,fgmask_diff)
    return dst


"""
Utility : 
        讀取影片
Input :
        None
Output:
        播放海豹ㄉ影片
        有聲音，但是聲音會先播放完：|
"""


def readViedo():

    video = cv2.VideoCapture(video_path)
    # player = MediaPlayer(video_path)
    fps = int(video.get(cv2.CAP_PROP_FPS))
    frame_nums = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    width, height = int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(
        video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter('movie/output1.mp4',
                          0x7634706d, fps, (width, height))
    ret, frame = video.read()
    for frame_idx in range(frame_nums):
        ret, frame = video.read()
        orgimg = frame
        if not ret:
            print("Can't not receive frame")
            break
        frame = cv2.flip(frame, 1)  # 圖片翻轉
        frame = img_process(frame, frame)
        out.write(frame)
        # audio_frame, val = player.get_frame()
        cv2.imshow('frame', frame)
        cv2.waitKey(1000//fps)
    video.release()
    out.release()
    cv2.destroyAllWindows()


def main():
    readViedo()


main()
