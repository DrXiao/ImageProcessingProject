import numpy as np
import cv2
import time
from ffpyplayer.player import MediaPlayer
from PIL import Image
from matplotlib import pyplot
video_path = 'movie/seal.mp4'

##

##


def preprocess(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 灰階
    ret, img = cv2.threshold(img, 170, 255, cv2.THRESH_BINARY)  # 門檻
    return img


lastFrame = None
fgbg_mog = cv2.bgsegm.createBackgroundSubtractorMOG()
#fgbg_mog = cv2.createBackgroundSubtractorMOG(history=60, detectShadows=True)
fgbg_mog2 = cv2.createBackgroundSubtractorMOG2(detectShadows=True)
fgbg_knn = cv2.createBackgroundSubtractorKNN(detectShadows=True)
fgbg_gmg = cv2.bgsegm.createBackgroundSubtractorGMG()
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))


def img_process(img):

    global lastFrame
    frame_preprocess = preprocess(img)
    if(lastFrame is None):
        lastFrame = frame_preprocess
    fgmask_diff = np.uint8(cv2.absdiff(frame_preprocess, lastFrame))
    lastFrame = frame_preprocess
    fgmask_diff = cv2.cvtColor(fgmask_diff, cv2.COLOR_GRAY2BGR)

    # fgmask_mog = fgbg_mog.apply(frame_preprocess)
    # fgmask_mog2 = fgbg_mog2.apply(frame_preprocess)
    # fgmask_knn = fgbg_knn.apply(frame_preprocess)
    # fgmask_gmg = fgbg_gmg.apply(frame_preprocess)

    return fgmask_diff


"""
Utility : 
        讀取影片
Input :
        None
Output:
        播放海豹ㄉ影片
        有聲音，但是聲音會先播放完：|
"""


def readVideo_T0(filename='movie/output.mp4'):

    video = cv2.VideoCapture(video_path)
    # player = MediaPlayer(video_path)
    fps = int(video.get(cv2.CAP_PROP_FPS))
    frame_nums = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    width, height = int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(
        video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(filename,
                          0x7634706d, fps, (width, height))
    for frame_idx in range(frame_nums):
        ret, frame = video.read()
        if not ret:
            print("Can't not receive frame")
            break
        frame = np.uint8(img_process(frame))
        # audio_frame, val = player.get_frame()
        # cv2.imshow('frame', frame)
        out.write(frame)
        cv2.waitKey(1000//fps)
    video.release()
    out.release()
    cv2.destroyAllWindows()
