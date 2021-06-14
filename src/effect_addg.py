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
def readVideo_remove_point(filename='movie/output.mp4'):
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
        img = []
        dst,labels,mask,frame = remove_point(frame, 0.4, 60, 1500)
        dst,labels,mask,frame = remove_point(frame, 0.4, 40, 5000)
        dst,labels,mask,frame = remove_point(frame, 1, 40, 4000)
        
        # audio_frame, val = player.get_frame()
        out.write(frame)
        # cv2.imshow('frame', frame)
        cv2.waitKey(1000//fps)
    video.release()
    # out.release()
    cv2.destroyAllWindows()

def remove_point(frame, gamma, thres, maxarea):

    # 轉灰階
    src1 = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    # 直方圖均等
    # equal = cv2.equalizeHist(src1)

    # 把暗部拉開
    gamma_corrected = np.array(255*(src1 / 255) ** gamma, dtype = 'uint8')
    # 邊緣檢測
    x_gray = cv2.Sobel(gamma_corrected,cv2.CV_64F,1,0)
    y_gray = cv2.Sobel(gamma_corrected,cv2.CV_64F,0,1)
    x_gray = cv2.convertScaleAbs(x_gray)
    y_gray = cv2.convertScaleAbs(y_gray)
    dst = cv2.add(x_gray,y_gray,dtype=cv2.CV_16S)
    dst = cv2.convertScaleAbs(dst)
    # thres = 40
    dst[dst>thres]=255
    dst[dst<=thres]=0

    # 出事了阿伯
    # 閉運算把點先連起來
    labels = ((morphology.closing(dst, skimage.morphology.disk(3))>0)*255).astype(np.uint8)
    labels_out = labels
    num_labels,labels,stats,centers = cv2.connectedComponentsWithStats(labels, connectivity=4,ltype=cv2.CV_32S)
    for t in range(1, num_labels, 1):
        x, y, w, h, area = stats[t]
        if area>maxarea:
            index = np.where(labels==t)
            labels[index[0], index[1]] = 0

    mask = (labels>0).astype(np.uint8)*255

    mask = remove_holes_in_region(mask)
    frame = cv2.inpaint(frame,mask,10,cv2.INPAINT_TELEA)

    return dst, labels_out, mask, frame

# 把圈圈中間的空洞補齊
def remove_holes_in_region(mask_scar):
    cnts, _ = cv2.findContours(mask_scar.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in cnts:
        cnt = cnt.transpose(1,0,2) # (1,N,2) N:points number
        cv2.fillPoly(mask_scar, cnt, 1)
    return mask_scar