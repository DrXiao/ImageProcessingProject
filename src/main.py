import cv2

video_path = 'movie/seal.mp4'

"""
Utility : 
        讀取影片
Input :
        None
Output:
        播放海豹ㄉ影片
        暫時沒有聲音
"""
def readViedo():
    video = cv2.VideoCapture(video_path)

    fps = int(video.get(cv2.CAP_PROP_FPS))
    frame_nums = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    for frame_idx in range(frame_nums):
        ret, frame = video.read()
        if not ret:
            print("Can't not receive frame")
            break
        cv2.imshow('frame', frame)
        cv2.waitKey(1000//fps)
    video.release()
    cv2.destoryAllWindows()


def main():
    readViedo()


main()
