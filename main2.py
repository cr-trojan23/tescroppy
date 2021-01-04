import cv2
from PIL import Image
from pdf2image import convert_from_path
import pytesseract as pyt
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
        print("Converting " + "Page " + str(img_count) + " into image")
        img_count = img_count + 1
    print("Found " + str(img_count) + " pages")

def boundPara(img_name):
    image = cv2.imread(img_name)
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    threshold = cv2.threshold(grayscale, 0, 250, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    bound_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7,7))
    dilate_element = cv2.dilate(threshold, bound_kernel, iterations=6)
    contours = cv2.findContours(dilate_element, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    bounded_img = threshold
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        bounded_img = threshold[y:y+h, x:x+w]
        custom_conf = "--oem 1 --psm 1 -l eng --tessdata-dir \"/usr/share/tesseract-ocr/4.00/tessdata\""
        data = pyt.image_to_string(bounded_img, config=custom_conf)
        file_out = open("Extracted_Test.txt", "a")
        file_out.write(data)
        file_out.close

toImages(input("Enter PDF File location \n"))

for i in range(1, img_count):
    img_name = "page_" + str(i) + ".png"
    print("Processing ", img_name)
    boundPara(img_name)