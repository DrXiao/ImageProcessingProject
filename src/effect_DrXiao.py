import cv2
from ffpyplayer.player import MediaPlayer
from ffpyplayer.writer import MediaWriter
import numpy as np
import scipy.fft as fft
import math
video_path = 'movie/seal.mp4'

def basicfunc(frame):
    
    f = fft.fftshift(fft.fft2(frame))
    #print(f.shape)
    cv2.imwrite("origin.jpg", frame)
    original = 20 * np.log(np.abs(f))
    cv2.imwrite("origin_spectrum.jpg", original)
    mask = np.ones((frame.shape[0], frame.shape[1], 3), np.uint8)
    row, col = frame.shape[0]/2, frame.shape[1]/2
    # mask[int(row - row):int(row + row), int(col-5):int(col+5)] = 1
    f *= mask
    print(f.shape)
    spectrum = 20 * np.log(np.abs(f))
    cv2.imwrite("aftet_spectrum.jpg", spectrum)
    img_back = np.abs(fft.ifft2(fft.ifftshift(f)))
    cv2.imwrite("test.jpg", img_back)
    return img_back

yoffset = 4
yflag = True

def hidden_effect(frame):
    global yoffset, yflag
    
    if yoffset <= 2:
        yflag = True
    elif yoffset >= 36:
        yflag = False
    if yflag == True:
        yoffset += 1
    elif yflag == False:
        yoffset -= 1
    f = fft.fftshift(fft.fft2(frame))
    mask = np.ones((frame.shape[0], frame.shape[1], 3), np.uint8)
    row, col = frame.shape[0]/2, frame.shape[1]/2
    mask[int(row - row):int(row + row), int(col - yoffset):int(col - 2)] = 0
    mask[int(row - row):int(row + row), int(col + 2):int(col + yoffset)] = 0
    f *= mask
    spectrum = 20 * np.log(np.abs(f))
    img_back = np.abs(fft.ifft2(fft.ifftshift(f)))
    return img_back, spectrum

def readVideo_fake_hidden(filename='movie/output.mp4'):
    video = cv2.VideoCapture(video_path)
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_nums = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(filename, 0x7634706d, fps, (width, height))
    out2 = cv2.VideoWriter("movie/effect_spectrum1.mp4", 0x7634706d, fps, (width, height))
    fps = int(fps)
    for frame_idx in range(frame_nums):
        ret, frame = video.read()
        if not ret:
            print("Can't not receive frame")
            break
        frame, spectrum = hidden_effect(frame)
        out.write(np.uint8(frame))
        out2.write(np.uint8(spectrum))
        cv2.waitKey(1000//fps)
    video.release()
    out.release()
    cv2.destroyAllWindows()