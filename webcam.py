from scan import *
import main

print("=============================================")
print("=  c: Capture                               =")
print("=  q: Exit                                  =")
print("=============================================")


cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1440)
while(1):
    # get a frame
    ret, frame = cap.read()
    # show a frame
    cv2.imshow("capture", frame)

    input = cv2.waitKey(1) & 0xFF
    if input == ord('c'):
        image = frame
        cv2.imwrite("capture.jpg",image)
        
        print('Captured!')
        
        break
    
    if input == ord('q'):
        break

main.scanner(image)
img1=cv2.imread('ori.jpg')
img2=cv2.imread('transformed.jpg')
img3=cv2.imread('img_cnb.jpg')
cv2.imshow('Original',img1)
cv2.imshow('Transformed',img2)
cv2.imshow('CNB',img3)
cv2.waitKey(0)
cv2.destroyAllWindows()
cap.release()
cv2.destroyAllWindows()



