import cv2

def make_movie(time):
    fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
    video = cv2.VideoWriter('./movie/video.mp4', fourcc, 1.0, (640, 480))

    for i in range(0, time):
        img = cv2.imread('./movie/IMG_4357.PNG')
        img = cv2.resize(img, (640,480))
        video.write(img)

    video.release()