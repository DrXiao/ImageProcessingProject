import cv2

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
    video = cv2.VideoCapture('movie/seal.mp4')

    fps = int(video.get(cv2.CAP_PROP_FPS))
    size = (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    fNUMS = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    for frame_idx in range(fNUMS):
        ret, frame = video.read()
        if not ret:
            print("Can't not receive frame")
            break
        cv2.imshow('frame', frame)
        cv2.waitKey(1000//fps)
    video.release()


def main():
    readViedo()


main()
