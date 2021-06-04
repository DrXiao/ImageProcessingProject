import cv2
from ffpyplayer.player import MediaPlayer
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
def readViedo():
    video = cv2.VideoCapture(video_path)
    player = MediaPlayer(video_path)
    fps = int(video.get(cv2.CAP_PROP_FPS))
    frame_nums = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    for frame_idx in range(frame_nums):
        ret, frame = video.read()
        if not ret:
            print("Can't not receive frame")
            break
        cv2.imshow('frame', frame)
        cv2.waitKey(1000//fps)
        audio_frame, val = player.get_frame()
    video.release()
    cv2.destroyAllWindows()


def main():
    readViedo()


main()
