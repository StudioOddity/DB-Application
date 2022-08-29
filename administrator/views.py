import mysql
from django.shortcuts import render, redirect


# Create your views here.
from django.views.decorators.csrf import requires_csrf_token, csrf_exempt
from mysql.connector import ProgrammingError


@csrf_exempt
def administrator(request):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd='password',  # "mypassword",
        auth_plugin='mysql_native_password',
        database="university",
    )


    if 'Go Home' in request.POST:
        return redirect('home')

    if 'Go Back to Order' in request.POST:
        return render(request, 'adminsOrderView.html')

    if 'Go Back More' in request.POST:
        return render(request, 'adminsSelect.html')

    if 'Go Back to Login' in request.POST:
        return redirect('adminlogin')

    if 'ProfTeach' in request.POST:
        return render(request, 'adminsProfView.html')

    if 'Create Teaching List' in request.POST:
        searchsemester = request.POST.get('semester')
        searchyear = request.POST.get('year')

        mycursor = mydb.cursor(buffered=True)
        mycursor.execute('use university;')  # Select database

        mycursor.execute("SHOW TABLES LIKE 'ProfTeaching';")  # Search for tables with name matching criteria
        tableexistcheck = mycursor.rowcount  # Get the rowcount of the query

        if tableexistcheck == 0:
            mycursor.execute("CREATE TABLE ProfTeaching (Name varchar(200), Dept varchar(200), StudentNum int);")

        mycursor.execute("SELECT * FROM ProfTeaching;")
        datacheck = mycursor.rowcount

        if datacheck != 0:
            mycursor.execute("DELETE FROM ProfTeaching;")

        mycursor.execute(
            "INSERT INTO ProfTeaching (SELECT A.name, A.dept, count(*) FROM instructor A INNER JOIN teaches B on A.ID = B.ID INNER JOIN takes C on B.course_id = C.course_id AND B.sec_id = C.sec_id WHERE B.semester = '" + str(searchsemester) + "' AND C.semester = '" + str(searchsemester) + "' AND B.year = '" + str(searchyear) + "' AND C.year = '" + str(searchyear) + "' GROUP BY A.name);")
        mydb.commit()
        mycursor.execute("SELECT * from ProfTeaching WHERE Name IS NULL;")
        nullcheck = mycursor.rowcount; # Check if set has NULL

        if nullcheck == 0:
            mycursor.execute("SELECT A.name, A.dept, count(*) FROM instructor A INNER JOIN teaches B on A.ID = B.ID INNER JOIN takes C on B.course_id = C.course_id AND B.sec_id = C.sec_id WHERE B.semester = '" + str(searchsemester) + "' AND C.semester = '" + str(searchsemester) + "' AND B.year = '" + str(searchyear) + "' AND C.year = '" + str(searchyear) + "' GROUP BY A.name;")

            mycursor.execute(
                    "INSERT INTO ProfTeaching (SELECT name, dept, replace(count(*), 1, 0) FROM instructor GROUP BY name);")
            mycursor.execute("SELECT * FROM ProfTeaching;")
            data = '<table style="width:400px; border: 1px solid black; border-collapse: collapse"><tr><th>Name</th><th>Department</th><th>Number of Students</th></tr>'
            for (name, dept, num) in mycursor:
                r = ('<tr>' + \
                     '<td style="border: 1px solid black; border-collapse: collapse">' + str(name) + '</td>' + \
                     '<td style="border: 1px solid black; border-collapse: collapse">' + str(dept) + '</td>' + \
                     '<td style="border: 1px solid black; border-collapse: collapse">' + str(num) + '</td>' + \
                     '</tr>')
                data += r
            data += '</table>'

            dataworking = {'data': data}

            mycursor.close()
            mydb.close()

            return render(request, 'adminsProfResults.html', dataworking)


    if 'Salaries' in request.POST:
        mycursor = mydb.cursor(buffered=True)
        mycursor.execute('use university')  # Select database

        mycursor.execute("SHOW TABLES LIKE 'DeptSalaries'")  # Search for tables with name matching criteria
        tableexistcheck = mycursor.rowcount  # Get the rowcount of the query

        if tableexistcheck == 0:
            mycursor.execute("CREATE TABLE DeptSalaries (Dept varchar(200), Min int, Max int, Average int);")

        mycursor.execute("SELECT * FROM DeptSalaries;")
        datacheck = mycursor.rowcount

        if datacheck != 0:
            mycursor.execute("DELETE FROM DeptSalaries;")

        mycursor.execute("INSERT INTO DeptSalaries (SELECT dept, min(salary), max(salary), avg(salary) FROM instructor GROUP BY dept);")
        mydb.commit()
        mycursor.execute("SELECT dept, min(salary), max(salary), avg(salary) FROM instructor GROUP BY dept;")

        data = '<table style="width:400px; border: 1px solid black; border-collapse: collapse"><tr><th>Department</th><th>Min Salary</th><th>Max Salary</th><th>Average Salary</th></tr>'
        for (dept, min, max, avg) in mycursor:
            r = ('<tr>' + \
                 '<td style="border: 1px solid black; border-collapse: collapse">' + str(dept) + '</td>' + \
                 '<td style="border: 1px solid black; border-collapse: collapse">$' + str(min) + '</td>' + \
                 '<td style="border: 1px solid black; border-collapse: collapse">$' + str(max) + '</td>' + \
                 '<td style="border: 1px solid black; border-collapse: collapse">$' + str(avg) + '</td>' + \
                 '</tr>')
            data += r
        data += '</table>'

        dataworking = {'data': data}

        mycursor.close()
        mydb.close()

        return render(request, 'adminsSalaryResults.html', dataworking)

    if 'OrderBy' in request.POST:
        return render(request, 'adminsOrderView.html')

    if 'Create Table' in request.POST:
        namesort = request.POST.get('sort')

        if namesort == 'name':
            mycursor = mydb.cursor(buffered=True)
            mycursor.execute('use university')  # Select database

            mycursor.execute("SHOW TABLES LIKE 'ProfNameSort'")  # Search for tables with name matching criteria
            tableexistcheck = mycursor.rowcount  # Get the rowcount of the query

            if tableexistcheck == 0:
                mycursor.execute("CREATE TABLE ProfNameSort (ID int, Name varchar(200), Dept varchar(200), Salary int);")

            mycursor.execute("SELECT * FROM ProfNameSort;")
            datacheck = mycursor.rowcount

            if datacheck != 0:
                mycursor.execute("DELETE FROM ProfNameSort;")

            mycursor.execute("INSERT INTO ProfNameSort (SELECT * FROM instructor ORDER BY name);")
            mydb.commit()
            mycursor.execute("SELECT * FROM instructor ORDER BY name;")

            data = '<table style="width:400px; border: 1px solid black; border-collapse: collapse"><tr><th>ID</th><th>Name</th><th>Department</th><th>Salary</th></tr>'
            for (ID, name, dept, salary) in mycursor:
                r = ('<tr>' + \
                     '<td style="border: 1px solid black; border-collapse: collapse">' + str(ID) + '</td>' + \
                     '<td style="border: 1px solid black; border-collapse: collapse">' + str(name) + '</td>' + \
                     '<td style="border: 1px solid black; border-collapse: collapse">' + str(dept) + '</td>' + \
                     '<td style="border: 1px solid black; border-collapse: collapse">' + str(salary) + '</td>' + \
                     '</tr>')
                data += r
            data += '</table>'

            dataworking = {'data': data}

            mycursor.close()
            mydb.close()
            return render(request, 'adminsOrderResult.html', dataworking)

        if namesort == 'dept':
            mycursor = mydb.cursor(buffered=True)
            mycursor.execute('use university')  # Select database

            mycursor.execute("SHOW TABLES LIKE 'ProfDeptSort'")  # Search for tables with name matching criteria
            tableexistcheck = mycursor.rowcount  # Get the rowcount of the query

            if tableexistcheck == 0:
                mycursor.execute(
                    "CREATE TABLE ProfDeptSort (ID int, Name varchar(200), Dept varchar(200), Salary int);")

            mycursor.execute("SELECT * FROM ProfDeptSort;")
            datacheck = mycursor.rowcount

            if datacheck != 0:
                mycursor.execute("DELETE FROM ProfDeptSort;")

            mycursor.execute("INSERT INTO ProfDeptSort (SELECT * FROM instructor ORDER BY name);")
            mydb.commit()

            mycursor.execute("SELECT * FROM instructor ORDER BY dept;")

            data = '<table style="width:400px; border: 1px solid black; border-collapse: collapse"><tr><th>ID</th><th>Name</th><th>Department</th><th>Salary</th></tr>'
            for (ID, name, dept, salary) in mycursor:
                r = ('<tr>' + \
                     '<td style="border: 1px solid black; border-collapse: collapse">' + str(ID) + '</td>' + \
                     '<td style="border: 1px solid black; border-collapse: collapse">' + str(name) + '</td>' + \
                     '<td style="border: 1px solid black; border-collapse: collapse">' + str(dept) + '</td>' + \
                     '<td style="border: 1px solid black; border-collapse: collapse">' + str(salary) + '</td>' + \
                     '</tr>')
                data += r
            data += '</table>'

            dataworking = {'data': data}

            mycursor.close()
            mydb.close()
            return render(request, 'adminsOrderResult.html', dataworking)

        if namesort == 'salary':
            mycursor = mydb.cursor(buffered=True)
            mycursor.execute('use university')  # Select database

            mycursor.execute("SHOW TABLES LIKE 'ProfSalarySort'")  # Search for tables with name matching criteria
            tableexistcheck = mycursor.rowcount  # Get the rowcount of the query

            if tableexistcheck == 0:
                mycursor.execute(
                    "CREATE TABLE ProfSalarySort (ID int, Name varchar(200), Dept varchar(200), Salary int);")

            mycursor.execute("SELECT * FROM ProfSalarySort;")
            datacheck = mycursor.rowcount

            if datacheck != 0:
                mycursor.execute("DELETE FROM ProfSalarySort;")

            mycursor.execute("INSERT INTO ProfSalarySort (SELECT * FROM instructor ORDER BY name);")
            mydb.commit()

            mycursor.execute("SELECT * FROM instructor ORDER BY salary;")

            data = '<table style="width:400px; border: 1px solid black; border-collapse: collapse"><tr><th>ID</th><th>Name</th><th>Department</th><th>Salary</th></tr>'
            for (ID, name, dept, salary) in mycursor:
                r = ('<tr>' + \
                     '<td style="border: 1px solid black; border-collapse: collapse">' + str(ID) + '</td>' + \
                     '<td style="border: 1px solid black; border-collapse: collapse">' + str(name) + '</td>' + \
                     '<td style="border: 1px solid black; border-collapse: collapse">' + str(dept) + '</td>' + \
                     '<td style="border: 1px solid black; border-collapse: collapse">' + str(salary) + '</td>' + \
                     '</tr>')
                data += r
            data += '</table>'

            dataworking = {'data': data}

            mycursor.close()
            mydb.close()
            return render(request, 'adminsOrderResult.html', dataworking)

    return render(request, 'adminsSelect.html')

@requires_csrf_token
def adminlogin(request):
    # Example admin user:
    # Username: admin
    # Password: istrator

    global user
    global pwd

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
                return redirect('administrator')

            mycursor = mydb.cursor(buffered=True)
            mycursor.execute("USE UNIVERSITY;")
            mycursor.execute(
                "SELECT * FROM user WHERE Name = '" + str(user) + "' AND Role = 'Admin';") # Check if user has correct privileges
            privilegecheck = mycursor.rowcount

            if privilegecheck == 0: # If user does not have the right role, prevent login and reload
                error = "<h1>Invalid Privileges.</h1>"
                return render(request, 'adminLogin.html', {'error': error})

            else: # If user has the right role, allow login
                mycursor.close()
                mydb.close()
                return redirect('administrator')


        except ProgrammingError: # Exception raised if credentials are invalid, so display an error message
            error = "<h1>Invalid Credentials.</h1>"
            return render(request, 'adminLogin.html', {'error': error})
    if 'Go Home' in request.POST:
        return redirect('home')

    return render(request, 'adminLogin.html')
