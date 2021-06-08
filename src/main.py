import cv2
from ffpyplayer.player import MediaPlayer
from ffpyplayer.writer import MediaWriter
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


def readVideo(filename='movie/output.mp4'):
    video = cv2.VideoCapture(video_path)
    player = MediaPlayer(video_path)
    fps = int(video.get(cv2.CAP_PROP_FPS))
    frame_nums = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    width, height = int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(
        video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(filename, 0x7634706d, fps, (width, height))
    for frame_idx in range(frame_nums):
        ret, frame = video.read()
        if not ret:
            print("Can't not receive frame")
            break
        frame = cv2.flip(frame, 1)
        audio_frame, val = player.get_frame()
        out.write(frame)
        cv2.imshow('frame', frame)
        cv2.waitKey(1000//fps)
    video.release()
    out.release()
    cv2.destroyAllWindows()


def function(frame, filp_num=1):
    return cv2.flip(frame, filp_num)


def main():
    readVideo(function)


main()
