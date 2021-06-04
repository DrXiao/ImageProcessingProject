import cv2


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
    print("hello world")
    readViedo()


main()
