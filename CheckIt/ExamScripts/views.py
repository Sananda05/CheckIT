from os import read
from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount
from easyocr.easyocr import Reader
from FrontEnd.models import UserPictures, UserDetails

from .models import Courses, Exams, ExamScripts, ScriptDetails

from io import StringIO
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdf2image import convert_from_path

from IPython.display import display, Image

from easyocr import Reader

import numpy as np
import spacy
import PIL

from PIL import ImageDraw

import datetime
import xlwt

import pyparsing as pp

def ExamView(request, coursename, examname):
    if request.user.is_authenticated :
        users = User.objects.get( username = request.user )
        userPictures = UserPictures.objects.get( user = users.id )
        userDetails = UserDetails.objects.get( user_id = users.id )
        socialaccount_obj = SocialAccount.objects.filter( provider = 'google', user_id = users.id )
        courses = Courses.objects.get( name = coursename, owner_id_id = users.id )
        exam = Exams.objects.get( exam_name = examname, owner_id_id = users.id, course_id_id = courses.id )
        
        print(exam.exam_name)

        picture = "not available"
        no_picture = "not available"
        googleAcc = False

        if len(socialaccount_obj):
            picture = socialaccount_obj[0].extra_data['picture']
            googleAcc = True
        

        if request.method == "POST":
            pdf_name = request.FILES.getlist('exam_file')
            drive_pdf = request.POST['drive_pdf']
            drive_pdf_title = request.POST['drive_pdf_title']
            print(drive_pdf)
            print(drive_pdf_title)

            url = drive_pdf.rsplit("/", 1)[0]
            url = url + '/preview?usp=embed_googleplus'
            print(url)
            
            print(pdf_name)
            for file in pdf_name:
                ExamScripts.objects.create(pdf = file, owner_id_id = users.id, course_id_id = courses.id, exam_id_id = exam.id)
            
            if drive_pdf != "":
                ExamScripts.objects.create(pdf_from_drive = url, title = drive_pdf_title, owner_id_id = users.id, course_id_id = courses.id, exam_id_id = exam.id)
                
            return redirect("/home/"+ coursename + "/" + examname)
        
        else:
            examScripts = ExamScripts.objects.filter( exam_id_id = exam.id, owner_id_id = users.id, course_id_id = courses.id, is_Checked = False )
            file_names = []
            for i in examScripts:
                pdf_name = str(i.pdf).replace("Scripts/", "")
                file_names.append(pdf_name)
            
            print(file_names)
            zipped_lists = zip(examScripts, file_names)

            checkedExamScripts = ExamScripts.objects.filter( exam_id_id = exam.id, owner_id_id = users.id, course_id_id = courses.id, is_Checked = True )
            checked_file_names = []
            for i in checkedExamScripts:
                checked_pdf_name = str(i.pdf).replace("Scripts/", "")
                checked_file_names.append(checked_pdf_name)
            
            print(checked_file_names)
            zipped_lists_2 = zip(checkedExamScripts, checked_file_names)

            return render(request, 'src/Views/Exams/Exam.html', 
            {'user' : users, 'courses' : courses, 'exam' : exam, 'examScripts' : examScripts, 'checkedExamScripts' : checkedExamScripts, 
            "zipped_lists" : zipped_lists, "zipped_lists_2" : zipped_lists_2, 'userPictures' : userPictures, 'picture': picture,
            'no_picture': no_picture, 'googleAcc': googleAcc, 'userDetails': userDetails})
    else:
        return redirect("/login")

def ScriptView(request, coursename, examname, id):
    if request.user.is_authenticated :
        users = User.objects.get( username = request.user )
        userPictures = UserPictures.objects.get( user = users.id )
        userDetails = UserDetails.objects.get( user_id = users.id )
        socialaccount_obj = SocialAccount.objects.filter( provider = 'google', user_id = users.id )

        courses = Courses.objects.get( name = coursename, owner_id_id = users.id )
        exam = Exams.objects.get( exam_name = examname, owner_id_id = users.id, course_id_id = courses.id )
        examScript = ExamScripts.objects.get( id = id, exam_id_id = exam.id, owner_id_id = users.id, course_id_id = courses.id )
        script_details = ScriptDetails.objects.filter(Script_id_id = examScript.id)

        picture = "not available"
        no_picture = "not available"
        googleAcc = False

        if len(socialaccount_obj):
            picture = socialaccount_obj[0].extra_data['picture']
            googleAcc = True
        
        if request.method == "POST":
            Marks = request.POST['Marks']
            studentId = request.POST['studentId']
            marks_details = request.POST.getlist('field_name[]')
            ques_no = request.POST.getlist('ques_no[]')

            zipped_list = zip(marks_details, ques_no)
            print(zipped_list)

            ExamScripts.objects.filter( id = examScript.id ).update( student_id = studentId, is_Checked = True, Marks = Marks )
            for mark, ques in zipped_list:
                ScriptDetails.objects.create(ques_no = ques, Marks = mark, Script_id_id = examScript.id, exam_id_id = exam.id)

            return redirect("/home/"+ coursename + "/" + examname)
        else:
            print(examScript.id)
            examScripts = ExamScripts.objects.filter( exam_id_id = exam.id, owner_id_id = users.id, course_id_id = courses.id, is_Checked = False )

            rsrcmgr = PDFResourceManager()
            sio = StringIO()
            codec = "utf-8"
            laparams = LAParams()
            device = TextConverter(rsrcmgr, sio, codec=codec, laparams=laparams)
            interpreter = PDFPageInterpreter(rsrcmgr, device)   
            
            pdf_file  =  "D:\Projects\CheckIt\CheckIt" + exam.exam_question.url 

            # Extract text
            pdfFile = open(pdf_file, "rb")
            for page in PDFPage.get_pages(pdfFile):
                interpreter.process_page(page)
            
            pdfFile.close()
 
            # Return text from StringIO
            text = sio.getvalue()
 
            print(text)
 
            # Freeing Up
            device.close()
            sio.close()
        

            return render(request, 'src/Views/Exams/ExamScript.html', 
                {'user' : users, 'courses' : courses, 'exam' : exam, 'examScripts' : examScript, 'userPictures' : userPictures,
                'picture': picture, 'no_picture': no_picture, 'googleAcc': googleAcc, 'userDetails': userDetails,
                'script_details' : script_details, 'total_examScripts' : examScripts})
    else:
        return redirect("/login")

#def Uncheck(request, coursename, examname, student_id):
    if request.user.is_authenticated :
        users = User.objects.get( username = request.user )
        courses = Courses.objects.get( name = coursename, owner_id_id = users.id )
        exam = Exams.objects.get( exam_name = examname, owner_id_id = users.id, course_id_id = courses.id )
        examScript = ExamScripts.objects.get( student_id = student_id, exam_id_id = exam.id, owner_id_id = users.id, course_id_id = courses.id )

        ExamScripts.objects.filter( id = examScript.id ).update( is_Checked = False )

        return redirect("/home/"+ coursename + "/" + examname)
    
    else:
        return redirect("/login")

def Recheck(request, coursename, examname, id):
    if request.user.is_authenticated :
        users = User.objects.get( username = request.user )
        userPictures = UserPictures.objects.get( user = users.id )
        userDetails = UserDetails.objects.get( user_id = users.id )
        socialaccount_obj = SocialAccount.objects.filter( provider = 'google', user_id = users.id )

        courses = Courses.objects.get( name = coursename, owner_id_id = users.id )
        exam = Exams.objects.get( exam_name = examname, owner_id_id = users.id, course_id_id = courses.id )
        examScript = ExamScripts.objects.get( id = id, exam_id_id = exam.id, owner_id_id = users.id, course_id_id = courses.id )
        script_details = ScriptDetails.objects.filter(Script_id_id = examScript.id)

        picture = "not available"
        no_picture = "not available"
        googleAcc = False

        if len(socialaccount_obj):
            picture = socialaccount_obj[0].extra_data['picture']
            googleAcc = True

        if request.method == 'POST':
            Marks = request.POST['Marks']
            marks_details = request.POST.getlist('field_name[]')
            ques_no = request.POST.getlist('ques_no[]')

            ExamScripts.objects.filter( id = examScript.id ).update( is_Checked = True, Marks = Marks )

            zipped_list = zip(marks_details, ques_no)
            print(zipped_list)
            for mark, ques in zipped_list:
                if mark != "" and ques != "":                    
                    if ScriptDetails.objects.filter(Script_id_id = examScript.id, ques_no = ques).exists():
                        ScriptDetails.objects.filter( Script_id_id = examScript.id, ques_no = ques ).update( Marks = mark )
                    else:
                        ScriptDetails.objects.create(ques_no = ques, Marks = mark, Script_id_id = examScript.id, exam_id_id = exam.id)
                        
            return redirect("/home/"+ coursename + "/" + examname)

        else:
            examScripts = ExamScripts.objects.filter( exam_id_id = exam.id, owner_id_id = users.id, course_id_id = courses.id, is_Checked = False )
            
            return render(request, 'src/Views/Exams/EditMarks.html', {'user' : users, 'courses' : courses, 'exam' : exam,
            'userPictures' : userPictures, 'picture': picture, 'no_picture': no_picture, 'googleAcc': googleAcc, 'userDetails': userDetails,
            'examScripts' : examScript, 'script_details' : script_details, 'total_examScripts' : examScripts})
    
    else:
        return redirect("/login")

def ExportExcel (request, coursename, examname):
    if request.user.is_authenticated :
        users = User.objects.get( username = request.user )
        courses = Courses.objects.get( name = coursename, owner_id_id = users.id )
        exam = Exams.objects.get( exam_name = examname, owner_id_id = users.id, course_id_id = courses.id )

        response = HttpResponse(content_type = 'application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename = ' + courses.name + '-' + exam.exam_name + '-' + \
            str(datetime.datetime.now()) + '.xls'

        wb = xlwt.Workbook()
        ws = wb.add_sheet('Marksheet')

        #Heading
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = [ 'Student ID', 'Marks' ]

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
    
        #Data
        font_style = xlwt.XFStyle()
        rows = ExamScripts.objects.filter( exam_id_id = exam.id, owner_id_id = users.id, course_id_id = courses.id, is_Checked = True ).\
            values_list('student_id', 'Marks')
    
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, str(row[col_num]), font_style)
    
        wb.save(response)
        print(response)
        return response
    
    else:
        return redirect("/login")