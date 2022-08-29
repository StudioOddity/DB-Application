import mysql
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.csrf import requires_csrf_token, csrf_exempt
from mysql.connector import ProgrammingError

searchprofname = "test"


@requires_csrf_token
def professorlogin(request):
    global user
    global pwd

    # Example professor user
    # Username: Hou
    # Password: Databases

    if 'Login' in request.POST: # If login button is pressed
        # Get user input
        user = request.POST.get('username')
        pwd = request.POST.get('password')

        try: # Try to sign in with given credentials
            mydb = mysql.connector.connect(
                host="localhost",
                user=str(user),
                passwd=str(pwd),  # "mypassword",
                auth_plugin='mysql_native_password',
                database="university",
            )

            if str(user) == 'root': # For testing purposes, allow root access
                return redirect('professor')

            mycursor = mydb.cursor(buffered=True)
            mycursor.execute("USE UNIVERSITY;")
            mycursor.execute(
                "SELECT * FROM user WHERE Name = '" + str(user) + "' AND Role = 'Professor';")
            privilegecheck = mycursor.rowcount

            if privilegecheck == 0:
                error = "<h1>Invalid Privileges.</h1>"
                return render(request, 'professorLogin.html', {'error': error})

            else:
                searchprofname = request.session.get('searchprofname')
                request.session['searchprofname'] = str(user)
                mycursor.close()
                mydb.close()
                return redirect('professor')

        except ProgrammingError: # Exception raised if credentials are invalid, so display an error message
            error = "<h1>Invalid Credentials.</h1>"
            return render(request, 'professorLogin.html', {'error': error})
    if 'Go Home' in request.POST:
        return redirect('home')

    return render(request, 'professorLogin.html')


@csrf_exempt
def professor(request):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd='password',  # "mypassword",
        auth_plugin='mysql_native_password',
        database="university",
    )

    # These are all different redirects for Return buttons. Way to make this cleaner?

    if 'Go Home' in request.POST:
        return redirect('home')

    if 'Go Back' in request.POST:
        return render(request, 'professorsView.html')

    if 'Go Back More' in request.POST:
        return render(request, 'professorsSelect.html')

    if 'Go Back to Login' in request.POST:
        return redirect('professorlogin')

    if 'Go Back to Name' in request.POST:
        return render(request, 'professorsNameView.html')

    if 'NumStudent' in request.POST:
        return render(request, 'professorsView.html')

    if 'NameStudent' in request.POST:
        return render(request, 'professorsNameView.html')

    # List for Number of Students
    if 'Create List' in request.POST:
        # Get user input
        searchprofname = request.session.get('searchprofname')
        searchsemester = request.POST.get('semester')
        searchyear = request.POST.get('year')

        mycursor = mydb.cursor(buffered=True)
        mycursor.execute('use university') # Select database

        mycursor.execute("SHOW TABLES LIKE '" + str(searchprofname) + str(searchsemester) + str(
            searchyear) + "Number'")  # Search for tables with name matching criteria
        tableexistcheck = mycursor.rowcount  # Get the rowcount of the query

        if tableexistcheck == 0:  # If query returns an empty set, table does not exist, so create it
            mycursor.execute("CREATE TABLE " + str(searchprofname) + str(searchsemester) + str(
                searchyear) + "Number (course_id char(6), sec_id char(2), studentNum int)")
            mydb.commit()

        # Check the table that will be used to see if the results are already present
        mycursor.execute(
                "SELECT * FROM " + str(searchprofname) + str(searchsemester) + str(searchyear) + "Number WHERE (course_id, sec_id, studentNum) IN (SELECT A.course_id, A.sec_id, count(*) FROM takes A INNER JOIN teaches B on A.course_id = B.course_id and A.sec_id = B.sec_id INNER JOIN instructor C on B.ID = C.ID WHERE A.semester = '" + str(
                    searchsemester) + "' AND A.year = '" + str(searchyear) + "' AND B.semester = '" + str(
                    searchsemester) + "' AND B.year = '" + str(searchyear) + "' AND C.name = '" + str(
                    searchprofname) + "' GROUP BY A.sec_id);")
        existcheck = mycursor.rowcount

        if existcheck == 0: # If data doesn't exist
            # Insert it into the table
            mycursor.execute("INSERT INTO " + str(searchprofname) + str(searchsemester) + str(searchyear) + "Number (SELECT A.course_id, A.sec_id, count(*) FROM takes A INNER JOIN teaches B on A.course_id = B.course_id and A.sec_id = B.sec_id INNER JOIN instructor C on B.ID = C.ID WHERE A.semester = '" + str(searchsemester) + "' AND A.year = '" + str(searchyear) + "' AND B.semester = '" + str(searchsemester) + "' AND B.year = '" + str(searchyear) + "' AND C.name = '" + str(searchprofname) + "' GROUP BY A.sec_id);")
            mydb.commit()

            # Run query
            mycursor.execute("SELECT A.course_id, A.sec_id, count(*) FROM takes A INNER JOIN teaches B on A.course_id = B.course_id and A.sec_id = B.sec_id INNER JOIN instructor C on B.ID = C.ID WHERE A.semester = '" + str(
                        searchsemester) + "' AND A.year = '" + str(searchyear) + "' AND B.semester = '" + str(
                        searchsemester) + "' AND B.year = '" + str(searchyear) + "' AND C.name = '" + str(
                        searchprofname) + "' GROUP BY A.sec_id;")
            nullcheck = mycursor.rowcount
            if nullcheck != 0: # If results are found (query does not return an empty set)
                # Select the data
                mycursor.execute(
                    "SELECT A.course_id, A.sec_id, count(*) FROM takes A INNER JOIN teaches B on A.course_id = B.course_id and A.sec_id = B.sec_id INNER JOIN instructor C on B.ID = C.ID WHERE A.semester = '" + str(
                        searchsemester) + "' AND A.year = '" + str(searchyear) + "' AND B.semester = '" + str(
                        searchsemester) + "' AND B.year = '" + str(searchyear) + "' AND C.name = '" + str(
                        searchprofname) + "' GROUP BY A.sec_id;")

                # Put into a variable with HTML formatting
                data = '<table style="width:400px; border: 1px solid black; border-collapse: collapse"><tr><th>Course_ID</th><th>Section_ID</th><th>Number of Students</th></tr>'
                for (course_id, sec_ID, count) in mycursor:
                    r = ('<tr>' + \
                         '<td style="border: 1px solid black; border-collapse: collapse">' + str(course_id) + '</td>' + \
                        '<td style="border: 1px solid black; border-collapse: collapse">' + str(sec_ID) + '</td>' + \
                        '<td style="border: 1px solid black; border-collapse: collapse">' + str(count) + '</td>' + \
                        '</tr>')
                    data += r
                data += '</table>'

                dataworking = {'data': data}

                mycursor.close()
                mydb.close()
                # Pass data to template and render
                return render(request, 'professorsResult.html', dataworking)

            else:
                # Check if the table created contains any existing data
                mycursor.execute(
                    "SELECT * FROM " + str(searchprofname) + str(searchsemester) + str(searchyear) + "Number;")
                tableemptycheck = mycursor.rowcount
                if tableemptycheck == 0:  # If the table has no data, remove it to conserve space
                    mycursor.execute(
                        "DROP TABLE " + str(searchprofname) + str(searchsemester) + str(searchyear) + "Number;")

                error = "<h1>No results found matching the criteria.</h1>"
                return render(request, 'professorsView.html', {'error': error})
        else: # If data already exists, just display it
            mycursor.execute(
                "SELECT A.course_id, A.sec_id, count(*) FROM takes A INNER JOIN teaches B on A.course_id = B.course_id and A.sec_id = B.sec_id INNER JOIN instructor C on B.ID = C.ID WHERE A.semester = '" + str(
                    searchsemester) + "' AND A.year = '" + str(searchyear) + "' AND B.semester = '" + str(
                    searchsemester) + "' AND B.year = '" + str(searchyear) + "' AND C.name = '" + str(
                    searchprofname) + "' GROUP BY A.sec_id;")

            data = '<table style="width:400px; border: 1px solid black; border-collapse: collapse"><tr><th>Course_ID</th><th>Section_ID</th><th>Number of Students</th></tr>'
            for (course_id, sec_ID, count) in mycursor:
                r = ('<tr>' + \
                     '<td style="border: 1px solid black; border-collapse: collapse">' + str(course_id) + '</td>' + \
                     '<td style="border: 1px solid black; border-collapse: collapse">' + str(sec_ID) + '</td>' + \
                     '<td style="border: 1px solid black; border-collapse: collapse">' + str(count) + '</td>' + \
                     '</tr>')
                data += r
            data += '</table>'

            dataworking = {'data': data}

            mycursor.close()
            mydb.close()
            return render(request, 'professorsResult.html', dataworking)


    if 'Create Name List' in request.POST:
        # Table format will be 'ProfnameSemesterYearNames' i.e. 'Hou12020Names'

        ## Get User Input ##
        searchprofname = request.session.get('searchprofname')
        searchsemester = request.POST.get('semester')
        searchyear = request.POST.get('year')

        mycursor = mydb.cursor(buffered=True) # Set up cursor
        # Still need a where clause for user input
        # WHERE course_id LIKE search
        mycursor.execute("SHOW TABLES LIKE '" + str(searchprofname) + str(searchsemester) + str(searchyear) + "Names';") # Search for tables with name matching criteria
        tableexistcheck = mycursor.rowcount # Get the rowcount of the query

        if tableexistcheck == 0: # If query returns an empty set, table does not exist, so create it
            mycursor.execute("CREATE TABLE " + str(searchprofname) + str(searchsemester) + str(searchyear) + "Names (Name varchar(255));")
            mydb.commit()

        mycursor.execute('use university') # Select database
        # Check if data already exists in table
        mycursor.execute("SELECT * FROM " + str(searchprofname) + str(searchsemester) + str(searchyear) + "Names WHERE (name) IN (SELECT A.name FROM student A INNER JOIN takes B on A.ID = B.ID INNER JOIN teaches C on B.course_id = C.course_id AND B.sec_id = C.sec_id INNER JOIN instructor D on C.ID = D.ID WHERE B.semester = '" + str(searchsemester) + "' AND B.year = '" + str(searchyear) + "' AND C.semester = '" + str(searchsemester) + "' AND C.year = '" + str(searchyear) + "' AND D.Name = '" + str(searchprofname) + "');")
        existcheck = mycursor.rowcount # Get rowcount
        if existcheck == 0: # If table does not have the data
            # Insert data into table
            mycursor.execute("INSERT INTO " + str(searchprofname) + str(searchsemester) + str(searchyear) + "Names (SELECT A.name FROM student A INNER JOIN takes B on A.ID = B.ID INNER JOIN teaches C on B.course_id = C.course_id AND B.sec_id = C.sec_id INNER JOIN instructor D on C.ID = D.ID WHERE B.semester = '" + str(searchsemester) + "' AND B.year = '" + str(searchyear) + "' AND C.semester = '" + str(searchsemester) + "' AND C.year = '" + str(searchyear) + "' AND D.Name = '" + str(searchprofname) + "');")
            mydb.commit()
            # Check if query returned an empty set (no results)
            mycursor.execute("SELECT A.name FROM student A INNER JOIN takes B on A.ID = B.ID INNER JOIN teaches C on B.course_id = C.course_id AND B.sec_id = C.sec_id INNER JOIN instructor D on C.ID = D.ID WHERE B.semester = '" + str(searchsemester) + "' AND B.year = '" + str(searchyear) + "' AND C.semester = '" + str(searchsemester) + "' AND C.year = '" + str(searchyear) + "' AND D.Name = '" + str(searchprofname) + "';")
            nullcheck = mycursor.rowcount
            if nullcheck != 0: # If the query returns actual results, keep the data and store it in data2 variable in html formatting
                mycursor.execute("SELECT A.name FROM student A INNER JOIN takes B on A.ID = B.ID INNER JOIN teaches C on B.course_id = C.course_id AND B.sec_id = C.sec_id INNER JOIN instructor D on C.ID = D.ID WHERE B.semester = '" + str(searchsemester) + "' AND B.year = '" + str(searchyear) + "' AND C.semester = '" + str(searchsemester) + "' AND C.year = '" + str(searchyear) + "' AND D.Name = '" + str(searchprofname) + "';")
                data2 = '<table style="width:400px; border: 1px solid black; border-collapse: collapse"><tr><th>Student Names</th></tr>'
                for (name) in mycursor:
                    r = ('<tr>' + \
                         '<td style="border: 1px solid black; border-collapse: collapse">' + str(name) + '</td>' + \
                        '</tr>')
                    data2 += r
                data2 += '</table>'

                dataworking = {'data2': data2}
                mydb.commit()
                mycursor.close()
                mydb.close()
                return render(request, 'professorsNameResult.html', dataworking) # Pass the results to the template and redirect to show results
            else: # If no results found
                mycursor.execute("DELETE FROM " + str(searchprofname) + str(searchsemester) + str(searchyear) + "Names WHERE Name IS NULL;")
                # Check if the table created contains any existing data
                mycursor.execute("SELECT * FROM " + str(searchprofname) + str(searchsemester) + str(searchyear) + "Names;")
                tableemptycheck = mycursor.rowcount
                if tableemptycheck == 0: # If the table has no data, remove it to conserve space
                    mycursor.execute("DROP TABLE " + str(searchprofname) + str(searchsemester) + str(searchyear) + "Names;")

                # Return an error message and pass it to the same template, reloading page
                error = "<h1>No results found matching the criteria.</h1>"
                return render(request, 'professorsNameView.html', {'error': error})

        else: # If the data already exists
            # Just display it
            mycursor.execute("SELECT A.name FROM student A INNER JOIN takes B on A.ID = B.ID INNER JOIN teaches C on B.course_id = C.course_id AND B.sec_id = C.sec_id INNER JOIN instructor D on C.ID = D.ID WHERE B.semester = '" + str(searchsemester) + "' AND B.year = '" + str(searchyear) + "' AND C.semester = '" + str(searchsemester) + "' AND C.year = '" + str(searchyear) + "' AND D.Name = '" + str(searchprofname) + "';")
            data2 = '<table style="width:400px; border: 1px solid black; border-collapse: collapse"><tr><th>Student Names</th></tr>'
            for (name) in mycursor:
                r = ('<tr>' + \
                        '<td style="border: 1px solid black; border-collapse: collapse">' + str(name) + '</td>' + \
                        '</tr>')
                data2 += r
            data2 += '</table>'

            dataworking = {'data2': data2}
            mydb.commit()
            mycursor.close()
            mydb.close()
            return render(request, 'professorsNameResult.html', dataworking)

    return render(request, 'professorsSelect.html')





