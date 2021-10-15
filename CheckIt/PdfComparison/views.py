from django.shortcuts import redirect, render
from django.contrib.auth.models import User

from difflib import SequenceMatcher

from .models import uploaded_pdfFile,history, uploaded_multipleFile,uploaded_multipleFile1,multiple_history
from OCR_model.views import getText


from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import sys

# define path of tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

from pdf2image.exceptions import (
 PDFInfoNotInstalledError,
 PDFPageCountError,
 PDFSyntaxError
)

import os
from os import path
import shutil

from difflib import HtmlDiff

import pdfkit

from xhtml2pdf import pisa
from io import StringIO
from django.template.loader import get_template
from django.template import Context


rate =" "

i=0


# Create your views here.

def Multiplefiles(request):
    if request.user.is_authenticated :
        users = User.objects.get( username = request.user )

        if request.method == "POST":
            pdf = request.FILES.get('file1')
            otherfile = request.FILES.getlist('other_file')

            uploaded_multipleFile1.objects.create(pdf=pdf,owner_id_id = users.id)
           

            for file in otherfile:
                files = uploaded_multipleFile.objects.create(pdf=file, owner_id_id = users.id)
                
                multiple_history.objects.create(pdf1=pdf,pdf2= file,rate=" ", owner_id_id = users.id, pdf2_id_id = files.id)
            return redirect("/compare/multiplefiles")

        elif request.method == "GET":
            file = uploaded_multipleFile1.objects.filter(owner_id_id = users.id,is_compared=False)
            files = uploaded_multipleFile.objects.filter(owner_id_id = users.id,is_compared=False)
            totalfile = len(files)
            print(totalfile)
                    
            return render(request, 'src/Views/Comparison/Multiplefile.html' , {'file':file, 'files':files,'total':totalfile})


    else:
       return redirect("/login")     


def Twofiles(request):
    if request.user.is_authenticated :
        users = User.objects.get( username = request.user )
        
        if request.method == "POST":
                
                pdf = request.FILES.getlist('pdf_file')
                print(len(pdf))
                if len(pdf)>2:
                    alert="You can not upload more than two files!"
                    return render(request, 'src/Views/Comparison/PDF.html' , {'alert':alert})
                else:    

                    for file in pdf:
                        uploaded_pdfFile.objects.create( pdf=file,owner_id_id = users.id)
                    history.objects.create(pdf1=pdf[0],pdf2=pdf[1],rate=" ",owner_id_id = users.id)   
                    return redirect('/compare/twofiles')       
                
                
        elif request.method == "GET":
                    files = uploaded_pdfFile.objects.filter(owner_id_id = users.id,is_compared=False)
                    
                    return render(request, 'src/Views/Comparison/PDF.html' , {'files':files})
    else:
        return redirect("/login")


def deletePdf(request,id):
    file = uploaded_pdfFile.objects.get(id=id)
    file.delete()
    return redirect('/compare/twofiles')         

def ComparePdf(request):
    if request.user.is_authenticated :
        users = User.objects.get( username = request.user )
        files = uploaded_pdfFile.objects.filter(owner_id_id = users.id,is_compared=False)
        text=[]
        filename=[]

        if request == "POST":

            checkboxVal = request.POST.getlist["checkbox_val"]
            print(checkboxVal)
    

        for file in files:
            file_name, extension = os.path.splitext(str(file.pdf))
            print(extension)
            
        if extension == ".pdf":

            for file in files:
                getText(file.pdf)
            

            for file in files:

                file_name, extension = os.path.splitext(str(file.pdf))
                newfile = str(file_name).split("/")
                outfile = newfile[1]+".txt"

                out_file = "media/convertedfile/"+outfile
                f = open(out_file, "r")
                text.append( f.read())
                f.close()
            print(text)

        elif extension == ".txt":

            for file in files:
                outfile = "media/"+str(file.pdf)
                print(outfile)

                f = open(outfile, encoding="utf8")

                text.append(f.read())
                f.close()
        print(text[0])                    

        str1 = text[0]
        str2 = text[1]

        # comparing scripts
        seq = SequenceMatcher(None, str1,str2)

        list(seq.get_matching_blocks())

        result = seq.find_longest_match()

        rate = format(seq.ratio()*100, '.2f')
        state="disable"

        history.objects.filter(owner_id_id = users.id, rate=" ").update(rate=rate)

        for file in files:
            file_name, extension = os.path.splitext(str(file.pdf))
            i=0
            newfile = str(file_name).split("/")
            filename.insert(i,newfile[1])
            i=i+1
            

        with open("media/report_file/"+filename[0]+".txt", 'w') as f:
            f.write(str1)

        with open("media/report_file/"+filename[1]+".txt", 'w') as f:
            f.write(str2)    
        
        line1 = open("media/report_file/"+filename[0]+".txt").readlines()
        line2 = open("media/report_file/"+filename[1]+".txt").readlines()
        
        d = HtmlDiff()
        difference = d.make_file(line1,line2, filename[0]+".txt", filename[1]+".txt")
        report = open("Report.html","w")
        report.write(difference)
        report.close()    

        htmlstr = '<h2>Heading 2</h2><p>Sample paragraph.</p>'

    

        print(rate)
        return render(request,'src/Views/Comparison/PDF.html',{'files':files, 'rate':rate, 'state':state}) 

    else:
        return redirect("/login")


def CompareMultiple(request):

    if request.user.is_authenticated :
        users = User.objects.get( username = request.user )
        file1 = uploaded_multipleFile1.objects.filter(owner_id_id = users.id,is_compared=False)
        files = uploaded_multipleFile.objects.filter(owner_id_id = users.id,is_compared=False)
        text=[]
        totalfile= len(files)


        for file in files:
            file_name, extension = os.path.splitext(str(file.pdf))
            print(extension)
            
        if extension == ".pdf":

            for file in files:
                getText(file.pdf)
            

            for file in files:

                file_name, extension = os.path.splitext(str(file.pdf))
                newfile = str(file_name).split("/")
                outfile = newfile[1]+".txt"

                out_file = "media/convertedfile/"+outfile
                f = open(out_file, "r")
                text.append( f.read())
                f.close()
            print(text)

        elif extension == ".txt":
            for file in file1:
                mainfile = "media/"+str(file.pdf)
                f = open(mainfile, encoding="utf8")

                text1 = f.read()
                print(text1)

            for file in files:
                outfile = "media/"+str(file.pdf)
                print(outfile)

                f = open(outfile, encoding="utf8")

                text.append(f.read())
                f.close()
                
        print(text[0]) 
        file_counter = 0
        for i in files :

            str1 = text1
            str2 = text[file_counter]
            print(text[file_counter])
            file_counter= file_counter+1

            # comparing scripts
            seq = SequenceMatcher(None, str1,str2)

            list(seq.get_matching_blocks())

            result = seq.find_longest_match()

            rate = format(seq.ratio()*100, '.2f')
            print(rate)

            for file in files:
              multiple_history.objects.filter(pdf2=file,owner_id_id = users.id, rate=" ").update(rate=rate)
            
        result = multiple_history.objects.filter(owner_id_id = users.id)        

        return render(request,'src/Views/Comparison/Multiplefile.html',{'file':file1, 'files':files,'total':totalfile,'result':result})     


def reset(request):
    if request.user.is_authenticated :
        users = User.objects.get( username = request.user )

        files = uploaded_pdfFile.objects.filter(owner_id_id = users.id).update(is_compared=True)
        return redirect('/compare/twofiles')


def historyView(request):
    if request.user.is_authenticated :
        users = User.objects.get( username = request.user )
        files = history.objects.filter(owner_id_id = users.id)

        return render(request,'src/Views/Comparison/History.html',{'files':files})


def deleteHistory(request,id):
  
    file = history.objects.get(id=id)
    file.delete()
    return redirect('/comparison/history') 




     


         


