from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from tensorflow.python.ops.gen_logging_ops import Print
from django.http import HttpResponse, response
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

import mimetypes

from .models import pdfFiles,ConvertedPdfFile,HandWrittenFiles,ConvertedHandwrittenFile

from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import cv2
import sys

# define path of tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

from pdf2image.exceptions import (
 PDFInfoNotInstalledError,
 PDFPageCountError,
 PDFSyntaxError
)

from HTRmodel.views import getPdf
import os,io
import pandas as pd
from google.cloud import vision
from os import path 
import shutil

#Google Vision API
os.environ['GOOGLE_APPLICATION_CREDENTIALS']=r'VisionAPI_TOKEN.json'
client = vision.ImageAnnotatorClient()

# Create your views here.

def Handwrittenfiles(request):
 if request.user.is_authenticated :
    users = User.objects.get( username = request.user )
    
    if request.method == "POST":
            
            pdf = request.FILES.getlist('exam_file')
            print(pdf)
            for file in pdf:
                HandWrittenFiles.objects.create( pdf=file,owner_id_id = users.id)
            return redirect('/conversion/handwrittenfiles')       
            
            
    elif request.method == "GET":
                files = HandWrittenFiles.objects.filter(owner_id_id = users.id,is_converted=False)
                print(files)

                converted_files = ConvertedHandwrittenFile.objects.filter(owner_id_id = users.id)
                
                return render(request, 'src/Views/Conversion/HandwrittenFiles.html' , {'files':files, 'converted': converted_files})
 else:
     return redirect("/login")


def ConvertHandwrittenPdf(request,pdf):
    if request.user.is_authenticated:
       users = User.objects.get(username = request.user)
       file = HandWrittenFiles.objects.get(pdf="handwrittenfiles/"+ pdf,owner_id_id = users.id)
       print("-------Printing PDF-------")
       print(pdf)

       pdffile = "media/handwrittenfiles/"+pdf
       print(pdffile)

       file_name, extension = os.path.splitext(pdf)
       print(file_name)
    
       pages = convert_from_path(pdffile, 500)
       image_counter = 1

       for page in pages:
           page_name = "page_"+str(file_name)+str(image_counter)+".png"
           page.save(page_name, 'PNG')
           image_counter = image_counter + 1

       filelimit = image_counter-1
      
       outfile = file_name+".txt"
       f = open(outfile, "a")

       for i in range(1, filelimit + 1):
            
            filename = "page_"+str(file_name)+str(i)+".png"

            with io.open(filename, 'rb') as image_file:
                content = image_file.read()
            image = vision.Image(content=content)

            response = client.document_text_detection(image=image)
            docText = response.full_text_annotation.text
            print(docText)

            f.write(docText) 


        #    recog = getPdf(filename,users)
        #    print(recog)
        
        #    f.write(recog)
           

       f.close()

       for i in range(1, filelimit + 1):
                filename = "page_"+str(file_name)+str(i)+".png"
                original = 'C:/Users/ASUS/Desktop/DP/CheckIT/CheckIt/'+ filename
                target = r'C:\Users\ASUS\Desktop\DP\CheckIT\CheckIt\media\convertedImg'
                shutil.move(original,target)

       original = 'C:/Users/ASUS/Desktop/DP/CheckIT/CheckIt/'+ outfile
       target = r'C:\Users\ASUS\Desktop\DP\CheckIT\CheckIt\media\convertedfile'
       shutil.move(original,target)

       HandWrittenFiles.objects.filter(pdf="handwrittenfiles/"+pdf,owner_id_id= users.id).update(is_converted=True)
       ConvertedHandwrittenFile.objects.create(textfile=outfile,owner_id_id=users.id)
       
     
    # saving the file also in the local storage
    #    extend = file_name + ".text"
    #    converted_file = "convertedfile/" + extend

    #    convertedfile = ContentFile(recog)
       
          
       return redirect('/conversion/handwrittenfiles')



def DeleteWrittenConvertedFile(request,id):
    
    file = ConvertedHandwrittenFile.objects.get(id=id)
    file.delete()
    return redirect('/conversion/handwrittenfiles')    


def DeleteWrittenUnConvertedFile(request,id):

    file = HandWrittenFiles.objects.get(id=id)
    file.delete()
    return redirect('/conversion/handwrittenfiles')



def Pdffiles(request):
    if request.user.is_authenticated :
        users = User.objects.get( username = request.user )
        
        if request.method == "POST":
                
                pdf = request.FILES.getlist('exam_file')
                print(pdf)
                for file in pdf:
                    pdfFiles.objects.create( pdf=file,owner_id_id = users.id)
                return redirect('/conversion/pdffiles')       
                
                
        elif request.method == "GET":
                    files = pdfFiles.objects.filter(owner_id_id = users.id,is_converted=False)
                    print(files)

                    converted_files = ConvertedPdfFile.objects.filter(owner_id_id = users.id)
                    
                    return render(request, 'src/Views/Conversion/PdfFiles.html' , {'files':files, 'converted': converted_files})
    else:
        return redirect("/login")


def ConvertPdf(request,pdf):
    if request.user.is_authenticated:
       users = User.objects.get(username = request.user)

       file_name, extension = os.path.splitext(pdf)

       if extension == ".txt":
            print("it's already a Text File!")
            mssg = "It's already a Text File!"
            return render(request, 'src/Views/Conversion/PdfFiles.html' , {'mssg':mssg})
            
       else :
            print("------pdf------")
            print(pdf)

            PDF_file = "media/pdffiles/"+pdf

            pages = convert_from_path(PDF_file, 500)
            image_counter = 1

            for page in pages:
                filename = "page_"+str(pdf)+str(image_counter)+".jpg"
                page.save(filename, 'JPEG')
                image_counter = image_counter + 1

            filelimit = image_counter-1
            
            outfile = file_name+".txt"
            f = open(outfile, "a")

            for i in range(1, filelimit + 1):
                filename = "page_"+str(pdf)+str(i)+".jpg"
                img = cv2.imread(filename)

                # 2. Resize the image
                img = cv2.resize(img, None, fx=0.5, fy=0.5)
                # 3. Convert image to grayscale
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                # 4. Convert image to black and white (using adaptive threshold)
                adaptive_threshold = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 85, 11)
         
                text = str(((pytesseract.image_to_string(adaptive_threshold,config = "--psm 6"))))
                text = text.replace('-\n', '')
                f.write(text)
                
            f.close()

            for i in range(1, filelimit + 1):
                filename = "page_"+str(pdf)+str(i)+".jpg"
                original = 'C:/Users/ASUS/Desktop/DP/CheckIT/CheckIt/'+ filename
                target = r'C:\Users\ASUS\Desktop\DP\CheckIT\CheckIt\media\convertedImg'
                shutil.move(original,target)



            #changing directory converted file
            original = 'C:/Users/ASUS/Desktop/DP/CheckIT/CheckIt/'+ outfile
            target = r'C:\Users\ASUS\Desktop\DP\CheckIT\CheckIt\media\convertedfile'
            shutil.move(original,target)


            pdfFiles.objects.filter(pdf="pdffiles/"+pdf,owner_id_id= users.id).update(is_converted=True)
            ConvertedPdfFile.objects.create(textfile=outfile,owner_id_id=users.id)
       return redirect("/conversion/pdffiles")

def download_file(request,file_name):
   
    filename = file_name
    # Define the full file path
    filepath = 'media/convertedfile/' + filename
  
    path = open(filepath, 'r')
  
    mime_type, _ = mimetypes.guess_type(filepath)

    response = HttpResponse(path, content_type=mime_type)

    response['Content-Disposition'] = "attachment; filename=%s" % filename

    return response             
    

def DeleteConvertedFile(request,id):
    
    file = ConvertedPdfFile.objects.get(id=id)
    file.delete()
    return redirect('/conversion/pdffiles')    


def DeleteUnConvertedFile(request,id):

    file = pdfFiles.objects.get(id=id)
    file.delete()
    return redirect('/conversion/pdffiles')

