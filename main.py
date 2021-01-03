import cv2
from PIL import Image
from pdf2image import convert_from_path
import pytesseract
import sys
import os


def toImages(pdf_name):
    pages = convert_from_path(pdf_name, 300)
    global img_count
    img_count = 1
    for page in pages:
        img_name = "page_" + str(img_count) + ".png"
        page.save(img_name, "PNG")
        img_count = img_count + 1
    print(img_count)

def cropImages():
    for i in range(1, img_count):
        img_name = "page_" + str(i) + ".png"
        print(img_name)
        img_file = cv2.imread(img_name, cv2.IMREAD_GRAYSCALE)
        width, height = img_file.shape
        print(height, width)
        img_crop_left = img_file[0:height, 0:round(width/2)]
        img_crop_right = img_file[0:height, round(width/2):width]
        crop_left = "page_" + str(i) + "_left" + ".png"
        crop_right = "page_" + str(i) + "_right" + ".png"
        cv2.imwrite(crop_left, img_crop_left)
        cv2.imwrite(crop_right, img_crop_right)
        os.remove(img_name)


toImages("/home/kiaria/Documents/318- chp 22.pdf")
cropImages()