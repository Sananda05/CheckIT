from django.shortcuts import render

from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import os
import shutil

# define path of tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

from pdf2image.exceptions import (
 PDFInfoNotInstalledError,
 PDFPageCountError,
 PDFSyntaxError
)

# Create your views here.

def getText(file):

    print(file)
    PDF_file = "media/"+str(file)
    file_name, extension = os.path.splitext(str(file))
    newfile = str(file_name).split("/")
    print(newfile)

    pages = convert_from_path(PDF_file, 500)
    print(PDF_file)
    image_counter = 1
    textfile =[]

    for page in pages:
        print(page)

    for page in pages:
        filename = "page_"+str(newfile[1])+str(image_counter)+".jpg"
        page.save(filename, 'JPEG')
        image_counter = image_counter + 1

    filelimit = image_counter-1
    
    outfile = newfile[1]+".txt"
    f = open(outfile, "a")

    for i in range(1, filelimit + 1):
        filename = "page_"+str(newfile[1])+str(i)+".jpg"

        print(filename)
        
        text = str(((pytesseract.image_to_string(Image.open(filename)))))
        text = text.replace('-\n', '')
        f.write(text)
        
    f.close()

    original = 'C:/Users/ASUS/Desktop/DP/CheckIT/CheckIt/'+ outfile
    target = r'C:\Users\ASUS\Desktop\DP\CheckIT\CheckIt\media\convertedfile_comparison'
    shutil.move(original,target)

