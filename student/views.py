from django.contrib.auth import login, logout, authenticate, get_user_model
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import path
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token,csrf_protect
from django.http import HttpResponse
from django.template import RequestContext
from django import forms
from django.forms import ModelForm
from django.views.decorators.csrf import csrf_exempt
from string import Template
import mysql.connector

# Create your views here.
from mysql.connector import ProgrammingError


@csrf_exempt
def students(request):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd='password',  # "mypassword",
        auth_plugin='mysql_native_password',
        database="university",
    )

    if 'Go Home' in request.POST:
        return redirect('home')

    if 'Go Back' in request.POST:
        return render(request, 'studentsView.html')

    if 'Go Back More' in request.POST:
        return redirect('studentlogin')


    if 'Search' in request.POST:
        search = request.POST.get('department')
        searchsemester = request.POST.get('semester')
        searchyear = request.POST.get('year')

        mycursor = mydb.cursor(buffered=True)
        # Still need a where clause for user input
        # WHERE course_id LIKE search
        mycursor.execute('use university')
        mycursor.execute("SELECT * FROM section WHERE course_id LIKE '" + str(search) + "%' AND semester= '" + str(searchsemester) + "' AND year= '" + str(searchyear) + "';")
        nullcheck = mycursor.rowcount

        if nullcheck == 0:
            error = "<h1>No results found matching the criteria.</h1>"
            return render(request, 'studentsView.html', {'error': error})
        else:
            mycursor.execute("SELECT * FROM section WHERE course_id LIKE '" + str(search) + "%' AND semester= '" + str(
                searchsemester) + "' AND year= '" + str(searchyear) + "';")
            data = '<table style="width:400px; border: 1px solid black; border-collapse: collapse"><tr><th>Course_ID</th><th>Section_ID</th><th>Semester</th><th>Year</th><th>Building</th><th>Room</th><th>Capacity</th></tr>'
            for (course_id, sec_ID, semester, year, building, room, capacity) in mycursor:
                r = ('<tr>' + \
                    '<td style="border: 1px solid black; border-collapse: collapse">' + str(course_id) + '</td>' + \
                    '<td style="border: 1px solid black; border-collapse: collapse">' + str(sec_ID) + '</td>' + \
                    '<td style="border: 1px solid black; border-collapse: collapse">' + str(semester) + '</td>' + \
                     '<td style="border: 1px solid black; border-collapse: collapse">' + str(year) + '</td>' + \
                     '<td style="border: 1px solid black; border-collapse: collapse">' + building + '</td>' + \
                     '<td style="border: 1px solid black; border-collapse: collapse">' + str(room) + '</td>' + \
                     '<td style="border: 1px solid black; border-collapse: collapse">' + str(capacity) + '</td>' + \
                     '</tr>')
                data += r
            data += '</table>'

            dataworking = {'data': data}
            mycursor.close()
            mydb.close()
            return render(request, 'studentsResult.html', dataworking)
    return render(request, 'studentsView.html')

@requires_csrf_token
def studentlogin(request):
    global user
    global pwd

    # Example student user
    # Username: Carter
    # Password: Apple

    if 'Login' in request.POST:
        user = request.POST.get('username')
        pwd = request.POST.get('password')

        try: #try to sign in with given credentials
            mydb = mysql.connector.connect(
                host="localhost",
                user=str(user),
                passwd=str(pwd),  # "mypassword",
                auth_plugin='mysql_native_password',
                database="university",
            )

            if str(user) == 'root': # For testing purposes, allow root access
                return redirect('students')

            mycursor = mydb.cursor(buffered=True)
            mycursor.execute("USE UNIVERSITY;")
            mycursor.execute(
                "SELECT * FROM user WHERE Name = '" + str(user) + "' AND Role = 'Student';")
            privilegecheck = mycursor.rowcount

            if privilegecheck == 0:
                error = "<h1>Invalid Privileges.</h1>"
                return render(request, 'studentLogin.html', {'error': error})

            else:
                mycursor.close()
                mydb.close()
                return redirect('students')

        except ProgrammingError: #exception raised if credentials are invalid, so display an error message
            error = "<h1>Invalid Credentials.</h1>"
            return render(request, 'studentLogin.html', {'error': error})
    if 'Go Home' in request.POST:
        return redirect('home')

    return render(request, 'studentLogin.html')
