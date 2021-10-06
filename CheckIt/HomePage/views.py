from __future__ import print_function

import os 
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

import google_auth_oauthlib.flow
import google.oauth2.credentials

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from django.shortcuts import render, redirect
from django.contrib.auth import logout

from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount
from FrontEnd.models import UserPictures, UserDetails

from .models import Courses, Exams
from ExamScripts.models import ExamScripts

SCOPES = ['https://www.googleapis.com/auth/classroom.courses.readonly https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/classroom.coursework.me']

def HomePage(request):
    print (request.user)

    if request.user.is_authenticated :
        users = User.objects.get( username = request.user )
        userPictures = UserPictures.objects.get( user = users.id )
        userDetails = UserDetails.objects.get( user_id = users.id )
        socialaccount_obj = SocialAccount.objects.filter( provider = 'google', user_id = users.id )
        courses = Courses.objects.filter( owner_id_id = users.id )
        exams = Exams.objects.filter( owner_id_id = users.id )

        picture = "not available"
        no_picture = "not available"
        googleAcc = False

        if len(socialaccount_obj):
            picture = socialaccount_obj[0].extra_data['picture']
            googleAcc = True
        
        exam_count = []
        for course in courses:
            count = 0
            for exam in exams:
                if exam.course_id_id == course.id:
                    count = count + 1
            exam_count.append(count)
        
        if request.method == "POST":
            owner_id = users.id
                
            name = request.POST.get('name')
            CourseCode = request.POST.get('CourseCode')

            print(name)
            print(CourseCode)
                
            Courses.objects.create(name = name, CourseCode = CourseCode, owner_id_id = owner_id)
                
            print(users.username + " added Course " + name)

            return redirect('/home')
            
        else:
            zipped_lists = zip(courses, exam_count)
            return render(request, 'src/Views/Home/HomeContent.html', 
            {'user' : users, 'userPictures' : userPictures, 'courses' : courses, "zipped_lists" : zipped_lists,
            'picture': picture, 'no_picture': no_picture, 'googleAcc': googleAcc, 'userDetails': userDetails})
    else:
       return redirect("/login")

def GC_HomePage(request):
    print (request.user)

    if request.user.is_authenticated :
        users = User.objects.get( username = request.user )
        userPictures = UserPictures.objects.get( user = users.id )
        userDetails = UserDetails.objects.get( user_id = users.id )
        socialaccount_obj = SocialAccount.objects.filter( provider = 'google', user_id = users.id )
        courses = Courses.objects.filter( owner_id_id = users.id )
        exams = Exams.objects.filter( owner_id_id = users.id )

        picture = "not available"
        no_picture = "not available"
        googleAcc = False

        if len(socialaccount_obj):
            picture = socialaccount_obj[0].extra_data['picture']
            googleAcc = True
        
        exam_count = []
        for course in courses:
            count = 0
            for exam in exams:
                if exam.course_id_id == course.id:
                    count = count + 1
            exam_count.append(count)
        
        if request.method == "POST":
            owner_id = users.id
                
            name = request.POST.get('name')
            CourseCode = request.POST.get('CourseCode')

            print(name)
            print(CourseCode)
                
            Courses.objects.create(name = name, CourseCode = CourseCode, owner_id_id = owner_id)
                
            print(users.username + " added Course " + name)

            return redirect('/home')
        
        else:
            if 'credentials' not in request.session:
                return redirect('/authorize')
            
            credentials = google.oauth2.credentials.Credentials(
                **request.session['credentials'])
            
            service = build('classroom', 'v1', credentials = credentials)

            # Call the Classroom API
            results = service.courses().list(pageSize = 10).execute()
            gc_courses = results.get('courses', [])

            if not gc_courses:
                print('No courses found.')
            else:
                print('Courses:')
            for course in gc_courses:
                print(course)

            request.session['credentials'] = credentials_to_dict(credentials)
        #{   
            #if os.path.exists('token.json'):
            #    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
                # If there are no (valid) credentials available, let the user log in.
            #if not creds or not creds.valid:
            #    if creds and creds.expired and creds.refresh_token:
            #        creds.refresh(Request())
            #    else:
            #        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            #            'credentials.json', SCOPES)

            #        flow.redirect_uri = 'http://127.0.0.1:8000/oauth2callback'
            #        authorization_url, state = flow.authorization_url(
                        # Enable offline access so that you can refresh an access token without
                        # re-prompting the user for permission. Recommended for web server apps.
            #            access_type = 'offline',
                        # Enable incremental authorization. Recommended as a best practice.
            #            include_granted_scopes = 'true')
            #        creds = flow.credentials
            #        return redirect(authorization_url)
                
            #    state = flask.session['state']

            #    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            #        'client_secret.json',
            #        scopes=['https://www.googleapis.com/auth/drive.metadata.readonly'],
            #        state = state)
            #    flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

            #    authorization_response = flask.request.url
            #    flow.fetch_token(authorization_response=authorization_response)
                
            #    credentials = flow.credentials
            #    flask.session['credentials'] = {
            #        'token': credentials.token,
            #        'refresh_token': credentials.refresh_token,
            #        'token_uri': credentials.token_uri,
            #        'client_id': credentials.client_id,
            #        'client_secret': credentials.client_secret,
            #        'scopes': credentials.scopes}
                
                # Save the credentials for the next run
                #with open('token.json', 'w') as token:
                #    token.write(creds.to_json())
        #}
            zipped_lists = zip(courses, exam_count)
            return render(request, 'src/Views/Home/Classroom-Courses.html', 
            {'user' : users, 'userPictures' : userPictures, 'courses' : gc_courses, "zipped_lists" : zipped_lists,
            'picture': picture, 'no_picture': no_picture, 'googleAcc': googleAcc, 'userDetails': userDetails})
    else:
       return redirect("/login")

def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }

def GC_authorize(request):
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      'credentials.json', scopes = SCOPES)
    
    flow.redirect_uri = 'http://127.0.0.1:8000/oauth2callback'
    
    authorization_url, state = flow.authorization_url(
        access_type = 'online',
        approval_prompt = 'force',
        include_granted_scopes = 'true')
    
    request.session['state'] = state
    
    return redirect(authorization_url)

def GC_oauth2callback(request):
    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.
    state = request.session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'credentials.json', scopes = SCOPES, state = state)
    flow.redirect_uri = 'http://127.0.0.1:8000/oauth2callback'

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    print(request)
    authorization_response = request.get_full_path()
    
    flow.fetch_token(authorization_response = authorization_response)

    # Store credentials in the session.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    credentials = flow.credentials
    request.session['credentials'] = credentials_to_dict(credentials)

    return redirect('/home-classroom')

def CourseView(request, coursename):
    if request.user.is_authenticated :
        users = User.objects.get( username = request.user )
        socialaccount_obj = SocialAccount.objects.filter( provider = 'google', user_id = users.id )
        userPictures = UserPictures.objects.get( user = users.id )

        courses = Courses.objects.get( name = coursename, owner_id_id = users.id )
        exams = Exams.objects.filter( owner_id_id = users.id, course_id_id = courses.id )
        scripts = ExamScripts.objects.filter( owner_id_id = users.id, course_id_id = courses.id )
        
        picture = "not available"
        no_picture = "not available"
        googleAcc = False

        if len(socialaccount_obj):
            picture = socialaccount_obj[0].extra_data['picture']
            googleAcc = True
        
        script_count = []
        for exam in exams:
            count = 0
            for script in scripts:
                if script.exam_id_id == exam.id:
                    count = count + 1
            script_count.append(count)
        print(script_count)
        
        if request.method == "POST":
            owner_id = users.id
            course_id = courses.id

            exam_name = request.POST.get('exam_name')
            exam_question = request.FILES.get('exam_question')

            print(exam_name)
            print(exam_question)
                
            #Exams.objects.create(exam_name = exam_name, course_id_id = course_id, owner_id_id = owner_id)
            Exams.objects.create(exam_name = exam_name, exam_question = exam_question, course_id_id = course_id, owner_id_id = owner_id)
                
            print(users.username + " added exam " + exam_name + " under course " + courses.name)

            return redirect('/home/'+ courses.name)
        else:
            zipped_lists = zip(exams, script_count)
            return render(request, 'src/Views/Home/Course.html', 
            {'user' : users, 'userPictures': userPictures,  'coursename' : courses.name, 'exams' : exams, "zipped_lists" : zipped_lists,
            'picture': picture, 'no_picture': no_picture, 'googleAcc': googleAcc})
    else:
        return redirect("/login")

def GC_CourseView(request, course_id):
    if request.user.is_authenticated :
        users = User.objects.get( username = request.user )
        socialaccount_obj = SocialAccount.objects.filter( provider = 'google', user_id = users.id )
        userPictures = UserPictures.objects.get( user = users.id )

        #courses = Courses.objects.get( name = coursename, owner_id_id = users.id )
        #exams = Exams.objects.filter( owner_id_id = users.id, course_id_id = courses.id )
        #scripts = ExamScripts.objects.filter( owner_id_id = users.id, course_id_id = courses.id )
        
        picture = "not available"
        no_picture = "not available"
        googleAcc = False

        if len(socialaccount_obj):
            picture = socialaccount_obj[0].extra_data['picture']
            googleAcc = True
        
        if request.method == "POST":
            owner_id = users.id
            #course_id = courses.id

            exam_name = request.POST.get('exam_name')
            exam_question = request.FILES.get('exam_question')

            print(exam_name)
            print(exam_question)
                
            Exams.objects.create(exam_name = exam_name, exam_question = exam_question, course_id_id = course_id, owner_id_id = owner_id)

            return redirect('/home/'+ course_id)
        else:
            if 'credentials' not in request.session:
                return redirect('/authorize')
                   
            credentials = google.oauth2.credentials.Credentials(
                **request.session['credentials'])
        
            service = build('classroom', 'v1', credentials = credentials)

            # Call the Classroom API
            results = service.courses().courseWork().list(courseId = course_id, courseWorkStates = 'PUBLISHED', orderBy = 'dueDate asc',  pageSize = 10).execute()
            courseWorks = results.get('courseWork', [])

            if not courseWorks:
                print('No Course Works found.')
            else:
                print('Courses:')
            for courseWork in courseWorks:
                print(courseWork['title'])

            request.session['credentials'] = credentials_to_dict(credentials)
            
            #zipped_lists = zip(exams, script_count)
            return render(request, 'src/Views/GClassroom/G_Courses.html', 
            {'user' : users, 'userPictures': userPictures,  'courseWorks' : courseWorks, #'exams' : exams, "zipped_lists" : zipped_lists,
            'picture': picture, 'no_picture': no_picture, 'googleAcc': googleAcc})
    else:
        return redirect("/login")

def Logout(request):
    print (request.user, "logging out")

    if request.method == "POST":
       return render(request, 'src/Views/Home/Homepage.html') 
    else:
       logout(request)
       return redirect("/login")

def SetProfile(request):
    print (request.user)

    if request.user.is_authenticated :
        users = User.objects.get( username = request.user )
        userPictures = UserPictures.objects.get( user = users.id )
        userDetails = UserDetails.objects.get( user_id = users.id )
        socialaccount_obj = SocialAccount.objects.filter( provider = 'google', user_id = users.id )        
        
        picture = "not available"
        no_picture = "not available"
        googleAcc = False

        if len(socialaccount_obj):
            picture = socialaccount_obj[0].extra_data['picture']
            googleAcc = True        
        
        if request.method == "POST":
            owner_id = users.id
                
            name = request.POST.get('name')
            CourseCode = request.POST.get('CourseCode')

            print(name)
            print(CourseCode)
                
            Courses.objects.create(name = name, CourseCode = CourseCode, owner_id_id = owner_id)
                
            print(users.username + " added Course " + name)

            return redirect('/home')
            
        else:
            return render(request, 'src/Views/Users/NewUser.html', 
            {'user' : users, 'userPictures' : userPictures, 'picture': picture, 'no_picture': no_picture,
             'googleAcc': googleAcc, 'userDetails': userDetails})
    else:
       return redirect("/login")