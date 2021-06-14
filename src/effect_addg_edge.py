import cv2
from ffpyplayer.player import MediaPlayer
from ffpyplayer.writer import MediaWriter
import matplotlib.pyplot as plt
import numpy as np
import skimage
from skimage import morphology
video_path = 'movie/seal.mp4'

"""
Utility : 
        讀取影片
Input :
        None
Output:
        播放海豹ㄉ影片
        有聲音，但是聲音會先播放完：|
"""
def readVideo_edgeDetection(filename='movie/output_edgeDetection.mp4'):
    video = cv2.VideoCapture(video_path)
    #player = MediaPlayer(video_path)
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_nums = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(filename, 0x7634706d, fps, (width, height))
    fps = int(fps)

    for frame_idx in range(frame_nums):
        ret, frame = video.read()
        if not ret:
            print("Can't not receive frame")
            break
        #frame = img.copy()
        frame = edgeDetection(frame)
        # audio_frame, val = player.get_frame()
        out.write(np.uint8(frame))
        #cv2.imshow('frame', frame)
        cv2.waitKey(1000//fps)
    video.release()
    out.release()
    cv2.destroyAllWindows()

def edgeDetection(frame):
    src = frame # cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    x_gray = cv2.Sobel(src,cv2.CV_64F,1,0)
    y_gray = cv2.Sobel(src,cv2.CV_64F,0,1)
    x_gray = cv2.convertScaleAbs(x_gray)
    y_gray = cv2.convertScaleAbs(y_gray)
    dst = cv2.add(x_gray,y_gray,dtype=cv2.CV_8U)
    dst = cv2.convertScaleAbs(dst)

    return dst
