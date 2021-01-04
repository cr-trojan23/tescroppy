import cv2
from PIL import Image
from pdf2image import convert_from_path
import pytesseract
import sys
import os
import numpy


def toImages(pdf_name):
    pages = convert_from_path(pdf_name, 300)
    global img_count
    img_count = 1
    for page in pages:
        img_name = "page_" + str(img_count) + ".png"
        page.save(img_name, "PNG")
        img_count = img_count + 1
    print(img_count)

def boundPara(img_name):
    image = cv2.imread(img_name)
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    threshold = cv2.threshold(grayscale, 0, 250, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    bound_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7,7))
    dilate_element = cv2.dilate(threshold, bound_kernel, iterations=6)
    contours = cv2.findContours(dilate_element, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print(len(contours))
    contours = contours[0] if len(contours) == 2 else contours[1]
    print(len(contours))
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        print(x,y,w,h)
        cv2.rectangle(image, (x,y), (x+w, y+h), (255, 0 ,0), 2)
    cv2.imwrite("cont.png", image)
#toImages("/home/kiaria/Documents/318- chp 22.pdf")
boundPara("/home/kiaria/Documents/github_projects/tescroppy/page_2.png")