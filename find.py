import cv2

def set_res(cap, x,y):
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(x))
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(y))
    return str(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),str(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

cap = cv2.VideoCapture(1)
for x in range(3000,4000):
    for y in range (4000,4000):
        res = set_res(cap,x,y)
        print (res)
