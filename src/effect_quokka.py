import cv2
from ffpyplayer.player import MediaPlayer
from ffpyplayer.writer import MediaWriter
import numpy as np
import scipy.fft as fft
import math
import random
import os
video_path = 'movie/seal.mp4'

def changefirst(frame):
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)#顏色轉換->GRAY
    gray = cv2.medianBlur(gray, 7)#中值模糊
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 10)#域值
    color = cv2.bilateralFilter(frame, 12, 250, 250)
    frame = cv2.bitwise_and(color, color, mask=edges)
    return frame

def changeRGB(frame,lastbinary,flag):
    frame = changefirst(frame)
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)#顏色轉換->GRAY
    gray = cv2.medianBlur(gray, 7)#中值模糊
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 10)#域值
    gray = cv2.bitwise_not(gray,mask=edges)
    ret, binary = cv2.threshold(gray,127,255,cv2.THRESH_BINARY_INV)
    
    if flag != False:
        binarydiff = cv2.absdiff(binary,lastbinary)
    lastbinary = binary
    if flag != False:
        binary = binarydiff
    contours, hierarchy = cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    randomList=random.sample(range(0,255),3)
    if len(contours) > 400 :
        for i in range(400):
            frameRGB = cv2.drawContours(frame,contours,i,(randomList[0],randomList[1],randomList[2]),-1)
    elif len(contours) > 150:
        for i in range(150):
            frameRGB = cv2.drawContours(frame,contours,i,(randomList[0],randomList[1],randomList[2]),-1)
    elif len(contours) > 5:
        for i in range(5):
            frameRGB = cv2.drawContours(frame,contours,i,(randomList[0],randomList[1],randomList[2]),-1)
    frame = cv2.bitwise_and(frame,frameRGB)
    return frame,lastbinary

def floodfill(frame,height,width):
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)#顏色轉換->GRAY
    gray = cv2.medianBlur(gray, 7)#中值模糊
    mask=np.zeros([height+2 , width+2],np.uint8)
    loDiff = 20
    upDiff = 30
    cv2.floodFill(gray,mask,(int(height/2),int(width/2)),(255,0,0),(loDiff,loDiff,loDiff),(upDiff,upDiff,upDiff))
    #frame=cv2.bitwise_not(frame,msk)
    return frame


def readVideo_RGB(filename = 'movie/output_quokka.mp4'):
    video = cv2.VideoCapture(video_path)
    #player = MediaPlayer(video_path)
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_nums = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(filename, 0x7634706d, fps, (width, height))
    fps = int(fps)
    flag = True
    lastbinary= np.array
    for frame_idx in range(frame_nums):
        ret, frame = video.read()
        if not ret:
            print("Can't not receive frame")
            break
        frame=floodfill(frame,height,width)
        if frame_idx == 0:
            flag = False
        else:
            flag = True
        frame,lastbinary = changeRGB(frame,lastbinary,flag)
        # frame = cv2.flip(frame, 1)
        #audio_frame, val = player.get_frame()
        out.write(frame)
    video.release()
    out.release()
    cv2.destroyAllWindows()