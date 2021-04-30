from scan import *
import main
import time

cap = cv2.VideoCapture(1)
#cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1440)
while(1):
    global img_cnb
    # get a frame
    ret, frame = cap.read()
    # show a frame
    image = frame
    cv2.imshow('res',frame)
    input = cv2.waitKey(1) & 0xFF
    if input ==ord('q'):
        exit()

    # Preprocesss
    screenCnt, ratio = preProcess(image)
    
    if len(screenCnt) == 4:
        # apply the four point transform to obtain a top-down view of the original image
        transformed = transform(image, screenCnt.reshape(4,2) * ratio) # ? reshape(4,2)

        #Save Transformed Image
        cv2.imwrite('transformed.jpg',transformed)
        colorvalue = detect_color_image('transformed.jpg')
        # black and white image
        if colorvalue == 2:
            print('Black and White Image')
            ret,thresh1 = cv2.threshold(transformed,165,255,cv2.THRESH_BINARY)

            img_cnb = Contrast_and_Brightness(1.1,30,thresh1)

        # color image
        else:
            print('Color Image')
            #Contrast and Brightness Enhance
            img_cnb = Contrast_and_Brightness(1.1,30,transformed)


        cv2.imshow('enhanced',img_cnb)

        input = cv2.waitKey(1) & 0xFF
        if input ==ord('q'):
            exit()
