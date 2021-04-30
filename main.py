from scan import *

# function scanner
def scanner(image):
    #read
    if image is None:
        print("Open Image Failure！")
        exit()

    ori = image
    cv2.imwrite('ori.jpg',ori)

    # Preprocesss
    screenCnt, ratio = preProcess(image)
    if len(screenCnt) != 4:
        print("Edge Detect Error")
    else:
        # apply the four point transform to obtain a top-down view of the original image
        transformed = transform(image, screenCnt.reshape(4,2) * ratio) # ? reshape(4,2)

        #Save Transformed Image
        cv2.imwrite('transformed.jpg',transformed)

        colorvalue = detect_color_image('transformed.jpg')

        # black and white image
        if colorvalue == 2:
            print('Black and White Image')
            ret,thresh1 = cv2.threshold(transformed,165,255,cv2.THRESH_BINARY)
            cv2.imwrite('thresh1.jpg',thresh1)
            img_cnb = Contrast_and_Brightness(1.1,3,thresh1)
            cv2.imwrite('img_cnb.jpg',img_cnb)
        # color image
        else:
            print('Color Image')
            img_cnb = Contrast_and_Brightness(1.1,3,transformed)
            cv2.imwrite('img_cnb.jpg',img_cnb)

if __name__ == "__main__":
    file = 'capture.jpg'
    image = cv2.imread(file) #load image
    scanner(image)
        # display the image
    img1=cv2.imread('ori.jpg')
    img2=cv2.imread('transformed.jpg')
    img3=cv2.imread('img_cnb.jpg')
    cv2.imshow('Original',img1)
    cv2.imshow('Transformed',img2)
    cv2.imshow('CNB',img3)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
