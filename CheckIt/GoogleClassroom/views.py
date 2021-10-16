from __future__ import print_function

from django.shortcuts import render

# Create your views here.

import os

from .models import GC_ExamScripts, GC_ScriptDetails

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

SCOPES = ['https://www.googleapis.com/auth/classroom.courses \
        https://www.googleapis.com/auth/userinfo.profile \
        https://www.googleapis.com/auth/classroom.coursework.students \
        https://www.googleapis.com/auth/spreadsheets \
        https://www.googleapis.com/auth/drive \
        https://www.googleapis.com/auth/classroom.announcements']

def GC_HomePage(request):
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
        
        if 'credentials' not in request.session:
                return redirect('/authorize')
            
        credentials = google.oauth2.credentials.Credentials(
            **request.session['credentials'])
        
        service = build('classroom', 'v1', credentials = credentials)
        
        if request.method == "POST":
            name = request.POST.get('name')
            section = request.POST.get('section')
            subject = request.POST.get('subject')
            room = request.POST.get('room')

            course = {
                'name': name,
                'section': section,
                'descriptionHeading': name + ': ' + section,
                'description': subject,
                'room': room,
                'ownerId': 'me',
                'courseState': 'PROVISIONED'
            }

            course = service.courses().create(body=course).execute()

            return redirect('/home-classroom')
        
        else:
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

            return render(request, 'src/Views/Home/Classroom-Courses.html', 
            {'user' : users, 'userPictures' : userPictures, 'courses' : gc_courses,
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
    
    flow.redirect_uri = request.build_absolute_uri('/oauth2callback') #'http://127.0.0.1:8000/oauth2callback'
    
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
    flow.redirect_uri = request.build_absolute_uri('/oauth2callback') #'http://127.0.0.1:8000/oauth2callback'

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

def GC_CourseView(request, course_id):
    if request.user.is_authenticated :
        users = User.objects.get( username = request.user )
        socialaccount_obj = SocialAccount.objects.filter( provider = 'google', user_id = users.id )
        userPictures = UserPictures.objects.get( user = users.id )
        
        picture = "not available"
        no_picture = "not available"
        googleAcc = False

        if len(socialaccount_obj):
            picture = socialaccount_obj[0].extra_data['picture']
            googleAcc = True
        
        if 'credentials' not in request.session:
                return redirect('/authorize')
                   
        credentials = google.oauth2.credentials.Credentials(
            **request.session['credentials'])
        
        service = build('classroom', 'v1', credentials = credentials)
        
        if request.method == "POST":
            title = request.POST.get('title')
            points = request.POST.get('points')
            description = request.POST.get('description')
            gc_question = request.POST.get('gc_question')
            #exam_question = request.FILES.get('exam_question')
            
            print(title)
            print(points)
            print(description)
            print(gc_question)
            coursework = {
                'title': title,
                "assigneeMode": "ALL_STUDENTS",
                "associatedWithDeveloper": True,
                "description": description,
                "maxPoints": points, 
                "state": "PUBLISHED",
                'materials': [
                    {'link': {'url': gc_question}}
                ],
                "submissionModificationMode": "SUBMISSION_MODIFICATION_MODE_UNSPECIFIED",
                "workType": "ASSIGNMENT",
            }
            coursework = service.courses().courseWork().create(courseId = course_id, body = coursework).execute()
            
            #print('Assignment created with ID {%s}' % coursework.get('id'))

            return redirect('/home-classroom/'+ course_id)
        
        else:
            # Call the Classroom API
            results = service.courses().courseWork().list(courseId = course_id, courseWorkStates = 'PUBLISHED', 
                orderBy = 'dueDate asc',  pageSize = 10).execute()
            courseWorks = results.get('courseWork', [])

            if not courseWorks:
               print('No Course Works found.')
            else:
               print('Courses:')
               for courseWork in courseWorks:
                   print(courseWork)

            request.session['credentials'] = credentials_to_dict(credentials)
            
            return render(request, 'src/Views/GClassroom/G_Courses.html', 
            {'user' : users, 'userPictures': userPictures,  'courseWorks' : courseWorks, 'course_id' : course_id,
            'picture': picture, 'no_picture': no_picture, 'googleAcc': googleAcc})

    else:
        return redirect("/login")

def GC_submissions(request, course_id, courseWork_id):
    if request.user.is_authenticated :
        users = User.objects.get( username = request.user )
        socialaccount_obj = SocialAccount.objects.filter( provider = 'google', user_id = users.id )
        userPictures = UserPictures.objects.get( user = users.id )
        url = ''
        
        picture = "not available"
        no_picture = "not available"
        googleAcc = False

        if len(socialaccount_obj):
            picture = socialaccount_obj[0].extra_data['picture']
            googleAcc = True
        
        if request.method == "POST":
            
            text = request.POST.get('text')
            
            make_announcements(users, request, course_id, courseWork_id, text)
            
            return redirect('/home-classroom/'+ course_id)

        else:
            if 'credentials' not in request.session:
                return redirect('/authorize')
                   
            credentials = google.oauth2.credentials.Credentials(
                **request.session['credentials'])
        
            service = build('classroom', 'v1', credentials = credentials)

            # Call the Classroom API
            c_results = service.courses().courseWork().list(courseId = course_id, courseWorkStates = 'PUBLISHED', 
                orderBy = 'dueDate asc',  pageSize = 10).execute()
            s_results = service.courses().courseWork().studentSubmissions().list(courseId = course_id, courseWorkId = courseWork_id,
                states = 'TURNED_IN', late = 'NOT_LATE_ONLY', pageSize = 10).execute()
            #returned_results = service.courses().courseWork().studentSubmissions().list(courseId = course_id, courseWorkId = courseWork_id,
            #    states = 'RETURNED', late = 'NOT_LATE_ONLY', pageSize = 10).execute()
            
            submissions = s_results.get('studentSubmissions', [])
            returned_submissions = submissions
            courseWorks = c_results.get('courseWork', [])
            graded_sub = GC_ExamScripts.objects.filter( owner_id_id = users.id, courseID = course_id, courseWorkID = courseWork_id )
            
            graded = []
            for g in graded_sub:
                graded.append(g.scriptID)
            
            ungraded = []
            for submission in submissions:
                if submission['assignmentSubmission']['attachments'][0]['driveFile']['id'] not in graded:
                    ungraded.append(submission['assignmentSubmission']['attachments'][0]['driveFile']['id'])
            
            #print(ungraded)

            #if not returned_submissions:
            #    print('No Returned Submission Works found.')
            #else:
            #    print('Returned Submissions:')
            #    for submission in returned_submissions:
            #        print(submission)
            
            for courseWork in courseWorks:
                if courseWork_id == courseWork['id']:
                    old_url = courseWork['materials'][0]['driveFile']['driveFile']['alternateLink']
                    url = old_url.rsplit("/", 1)[0]
                    url = url + '/preview?usp=embed_googleplus'

                    courseWork_name = courseWork['title']

                    break
            
            request.session['credentials'] = credentials_to_dict(credentials)
            
            return render(request, 'src/Views/GClassroom/G_Submissions.html', 
            {'user' : users, 'course_id': course_id, 'userPictures': userPictures,  'submissions' : submissions, 'courseWork_name': courseWork_name, 'ungraded': ungraded,
            'picture': picture, 'graded_sub': graded_sub, 'no_picture': no_picture, 'googleAcc': googleAcc, 'url': url, 'returned_submissions': returned_submissions})
    else:
        return redirect("/login")

def GC_file(request, course_id, courseWork_id, script_id):
    if request.user.is_authenticated : 
        users = User.objects.get( username = request.user )
        socialaccount_obj = SocialAccount.objects.filter( provider = 'google', user_id = users.id )
        userPictures = UserPictures.objects.get( user = users.id )
        
        picture = "not available"
        no_picture = "not available"
        googleAcc = False

        if 'credentials' not in request.session:
                return redirect('/authorize')
                   
        credentials = google.oauth2.credentials.Credentials(
            **request.session['credentials'])
        
        service = build('classroom', 'v1', credentials = credentials)

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
            
            #grades = {
            #    'assignedGrade': Marks,
            #    'draftGrade': Marks
            #}
            #updateMask = 'assignedGrade, draftGrade'
            #url = 'https://classroom.googleapis.com/v1/courses/'+ course_id +'/courseWork/'+courseWork_id + '/studentSubmissions/'+ script_id + '/'
            #response = request.PATCH(url, json= grades, data={'updateMask': updateMask})
            #submission = service.courses().courseWork().studentSubmissions().get(
            #    courseId = course_id,
            #    courseWorkId = courseWork_id,
            #    id = script_id).execute()
            #submission.patch(
            #    body = grades,
            #    updateMask = 'assignedGrade, draftGrade').execute()
            
            #print(submission)
            #print('response')
            #print(response)

            GC_ExamScripts.objects.create(owner_id_id = users.id, scriptID = script_id, student_id = studentId, 
                courseID = course_id, courseWorkID = courseWork_id, is_Checked = True, Marks = Marks)
            GC_script = GC_ExamScripts.objects.get(scriptID = script_id)
            
            for mark, ques in zipped_list:
                GC_ScriptDetails.objects.create(ques_no = ques, Marks = mark, script = script_id, Script_id_id = GC_script.id)
            
            #service.courses().courseWork().studentSubmissions().return_(
            #    courseId = course_id,
            #    courseWorkId = courseWork_id,
            #    id = script_id
            #).execute()
            
            return redirect("/home-classroom/"+ course_id + "/" + courseWork_id)
        
        else:
            # Call the Classroom API
            results = service.courses().courseWork().studentSubmissions().list(courseId = course_id, courseWorkId = courseWork_id,
                states = 'TURNED_IN', late = 'NOT_LATE_ONLY', pageSize = 10).execute()
            c_results = service.courses().courseWork().list(courseId = course_id, courseWorkStates = 'PUBLISHED', 
                orderBy = 'dueDate asc',  pageSize = 10).execute()
            
            submissions = results.get('studentSubmissions', [])
            courseWorks = c_results.get('courseWork', [])
            
            for courseWork in courseWorks:
                if courseWork_id == courseWork['id']:
                    old_url = courseWork['materials'][0]['driveFile']['driveFile']['alternateLink']
                    ques_url = old_url.rsplit("/", 1)[0]
                    ques_url = ques_url + '/preview?usp=embed_googleplus'

                    course_Work = courseWork

                    break

            if not submissions:
                print('No Submission Works found.')
            
            else:
                print('Submissions:')
                for submission in submissions:
                    print(submission)
                    assignmentSubmission_id = submission['assignmentSubmission']['attachments'][0]['driveFile']['id']
                    if assignmentSubmission_id == script_id:
                        old_url = submission['assignmentSubmission']['attachments'][0]['driveFile']['alternateLink']
                        url = old_url.rsplit("/", 1)[0]
                        url = url + '/preview?usp=embed_googleplus'

                        script = submission['assignmentSubmission']['attachments'][0]['driveFile']
                        print(script['title'])
                        
                        break

            return render(request, 'src/Views/GClassroom/G_Script.html', 
                {'user' : users, 'picture': picture, 'no_picture': no_picture, 'googleAcc': googleAcc, 'courseWork_id': courseWork_id, 'course_Work': course_Work,
                'course_id':course_id, 'courseWork_id': courseWork_id, 'submissions': submissions, 'url': url, 'userPictures': userPictures, 'ques_url': ques_url, 'script': script, 'script_id': script_id})
    else:
        return redirect("/login")

def GC_gradedFile(request, course_id, courseWork_id, script_id, id):
    if request.user.is_authenticated : 
        users = User.objects.get( username = request.user )
        socialaccount_obj = SocialAccount.objects.filter( provider = 'google', user_id = users.id )
        userPictures = UserPictures.objects.get( user = users.id )
        
        picture = "not available"
        no_picture = "not available"
        googleAcc = False

        if 'credentials' not in request.session:
                return redirect('/authorize')
                   
        credentials = google.oauth2.credentials.Credentials(
            **request.session['credentials'])
        
        service = build('classroom', 'v1', credentials = credentials)

        if len(socialaccount_obj):
            picture = socialaccount_obj[0].extra_data['picture']
            googleAcc = True

        if request.method == "POST":
            Marks = request.POST['Marks']
            marks_details = request.POST.getlist('field_name[]')
            ques_no = request.POST.getlist('ques_no[]')
            
            GC_ExamScripts.objects.filter( id = id ).update( is_Checked = True, Marks = Marks )

            zipped_list = zip(marks_details, ques_no)
            print(zipped_list)
            for mark, ques in zipped_list:
                if mark != "" and ques != "":                    
                    if GC_ScriptDetails.objects.filter(Script_id_id = id, ques_no = ques).exists():
                        GC_ScriptDetails.objects.filter( Script_id_id = id, ques_no = ques ).update( Marks = mark )
                    else:
                        GC_ScriptDetails.objects.create(ques_no = ques, Marks = mark, Script_id_id = id, script = script_id)
            
            return redirect("/home-classroom"+ "/" + course_id + "/" + courseWork_id)
        
        else:
            # Call the Classroom API
            results = service.courses().courseWork().studentSubmissions().list(courseId = course_id, courseWorkId = courseWork_id,
                states = 'TURNED_IN', late = 'NOT_LATE_ONLY', pageSize = 10).execute()
            c_results = service.courses().courseWork().list(courseId = course_id, courseWorkStates = 'PUBLISHED', 
                orderBy = 'dueDate asc',  pageSize = 10).execute()
            
            submissions = results.get('studentSubmissions', [])
            courseWorks = c_results.get('courseWork', [])
            
            for courseWork in courseWorks:
                if courseWork_id == courseWork['id']:
                    old_url = courseWork['materials'][0]['driveFile']['driveFile']['alternateLink']
                    ques_url = old_url.rsplit("/", 1)[0]
                    ques_url = ques_url + '/preview?usp=embed_googleplus'

                    course_Work = courseWork

                    break
            
            if not submissions:
                print('No Submission Works found.')
                Submission = ''
            
            else:
                print('Submissions:')
                for submission in submissions:
                    print(submission)
                    assignmentSubmission_id = submission['assignmentSubmission']['attachments'][0]['driveFile']['id']
                    if assignmentSubmission_id == script_id:
                        old_url = submission['assignmentSubmission']['attachments'][0]['driveFile']['alternateLink']
                        url = old_url.rsplit("/", 1)[0]
                        url = url + '/preview?usp=embed_googleplus'

                        script = submission['assignmentSubmission']['attachments'][0]['driveFile']
                        Submission = submission
                        
                        break
            
            script_details = GC_ScriptDetails.objects.filter(Script_id_id = id)
            examScript = GC_ExamScripts.objects.get(id = id)
            
            return render(request, 'src/Views/GClassroom/G_GradedScript.html', 
                {'user' : users, 'picture': picture, 'no_picture': no_picture, 'googleAcc': googleAcc, 'courseWork_id': courseWork_id, 'course_Work': course_Work, 'script': script,
                'course_id':course_id, 'Submission': Submission, 'url': url, 'userPictures': userPictures, 'ques_url': ques_url, 'script_details': script_details, 'examScript': examScript})
    else:
        return redirect("/login")

def make_announcements(users, request, course_id, courseWork_id, text):
    if 'credentials' not in request.session:
        return redirect('/authorize')
                   
    credentials = google.oauth2.credentials.Credentials(
        **request.session['credentials'])

    service = build('sheets', 'v4', credentials = credentials)
    gc_service = build('classroom', 'v1', credentials = credentials)
    
    results = gc_service.courses().courseWork().studentSubmissions().list(courseId = course_id, courseWorkId = courseWork_id,
        states = 'RETURNED', late = 'NOT_LATE_ONLY', pageSize = 10).execute()
    
    #submissions = results.get('studentSubmissions', [])
    course = gc_service.courses().get(id = course_id).execute()
    courseWork = gc_service.courses().courseWork().get(id = courseWork_id, courseId = course_id).execute()

    graded_Submissions = GC_ExamScripts.objects.filter( owner_id_id = users.id )

    values = [
        ['ID', 'Marks'],
    ]
    for submission in graded_Submissions:
        list = []
        list.append(submission.student_id)
        list.append(submission.Marks)
        values.append(list)

    data = [{
        'range': 'A1:B200',
        'values': values
    }]
    body = {
        'valueInputOption': 'USER_ENTERED',
        'data': data
    }

    spreadsheet = {
        'properties': {
            'title': course['name'] + ': ' + courseWork['title']
        }
    }

    Spreadsheet = service.spreadsheets().create(body = spreadsheet).execute()
    add_value = service.spreadsheets().values().batchUpdate(
        spreadsheetId = Spreadsheet['spreadsheetId'],
        body = body).execute()
    
    print('yes')
    print(values)
    print(Spreadsheet)

    link = {
        'url': Spreadsheet['spreadsheetUrl']
    }

    materials = {
       "link": link
    }
    
    body = {
        'text': text,
        'materials': materials    
    }

    gc_service.courses().announcements().create(
        courseId = course_id,
        body = body   
    ).execute()
