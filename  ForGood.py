# -*- coding: utf-8 -*-

import cv2
import numpy as np
import pytesseract
from PIL import Image
import time

# Path of working folder on Disk
#src_path = "/home/adminivanov/rec"

def cut_img(img, size = 100):
    #TODO
    shape = img.shape
    print(shape, "Tw")
    mean_shape = list([i/2 for i in shape[:-1]])
    print(img)
    ret_img = img[mean_shape[0] - size/2:mean_shape[0] + size/2,
            mean_shape[1] - size/2:mean_shape[1] + size/2]

    return ret_img

def get_string(img):
    # Read image with opencv

    #img = cv2.imread("/home/adminivanov/rec/rec.png")
    # Convert to gray
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply dilation and erosion to remove some noise
    kernel =  np.ones((1 , 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations= 1)
    img = cv2.erode(img, kernel, iterations= 1)

    # Write image after removed noise
    #cv2.imwrite(src_path +  "removed_noise.png", img)

    # Apply threshold to get image with only black and white
    #img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

    # Write the image after apply opencv to do some ...
    #cv2.imwrite(src_path +  "thres.png", img)

    # Recognize text with tesseract for python
    result =  pytesseract.image_to_string(img)

    # Remove template file
    #os.remove(temp)

    return result



def run(code = 0):

    cap = cv2.VideoCapture(code)
 # Read image with opencv
    counter = 0
    max_counter = 100

    while True:
        ret, img = cap.read()
        cv2.imshow("camera", cut_img(img))

        if(counter % max_counter == 0 and counter > 0):
            text = get_string(cut_img(img, size = 100))
            counter = 0

            if(len(text) > 0):
                print(text)

        if cv2.waitKey(10) == 27: # Клавиша Esc
            break

        counter += 1
        time.sleep(1e-3)
 # Remove template file
    #os.remove(temp)

    cap.release()
    cv2.destroyAllWindows()

    print ("------ Done -------")

run()
