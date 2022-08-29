from django.http import HttpResponse
import mysql.connector
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from mysql.connector import ProgrammingError, DatabaseError


@csrf_exempt
def home(requests):
    if 'Studlog' in requests.POST:
        return redirect('studentlogin')
    if 'Proflog' in requests.POST:
        return redirect('professorlogin')
    if 'Adlog' in requests.POST:
        return redirect('adminlogin')
    if 'RegUser' in requests.POST:
        return redirect('registeruser')

    return render(requests, 'home.html')

def registeruser(requests):
    global user
    global pwd

    if 'Go Home' in requests.POST:
        return redirect('home')

    if 'Register' in requests.POST:
        user = requests.POST.get('username')
        pwd = requests.POST.get('password')
        roletype = requests.POST.get('role')

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd='KazumaK1ryu!',  # "mypassword",
            auth_plugin='mysql_native_password',
            database='university'
        )
        mycursor = mydb.cursor(buffered=True)
        mycursor.execute("USE UNIVERSITY;")
        mycursor.execute("select user AS role_name from mysql.user WHERE NOT LENGTH(authentication_string) AND user = 'admin';")
        rolecheck = mycursor.rowcount

        if rolecheck == 0:
            mycursor.execute("CREATE ROLE 'admin', 'professor', 'student';")
            mydb.commit()
            mycursor.execute("GRANT SELECT ON university.* TO 'student';")
            mydb.commit()
            mycursor.execute("GRANT INSERT, UPDATE, DELETE, SELECT ON university.* TO 'professor';")
            mydb.commit()
            mycursor.execute("GRANT ALL PRIVILEGES ON university.* TO 'admin';")
            mydb.commit()
        try:
            mycursor.execute("CREATE USER '" + str(user) + "'@'localhost' IDENTIFIED BY '" + str(pwd) + "';")
            mydb.commit()
        except DatabaseError:
            error = "<h1>User already exists.</h1>"
            return render(requests, 'registeruser.html', {'error': error})

        if roletype == 'admin':
            mycursor.execute("GRANT 'admin' TO '" + str(user) + "'@'localhost';")
            mydb.commit()

        if roletype == 'professor':
            mycursor.execute("GRANT 'professor' TO '" + str(user) + "'@'localhost';")
            mydb.commit()

        if roletype == 'student':
            mycursor.execute("GRANT 'student' TO '" + str(user) + "'@'localhost';")
            mydb.commit()

        mycursor.execute("FLUSH PRIVILEGES;")
        mydb.commit()
        mycursor.execute("SET GLOBAL ACTIVATE_ALL_ROLES_ON_LOGIN = 1;")
        mydb.commit()

        mycursor.execute("SHOW TABLES LIKE 'user';")
        usertablecheck = mycursor.rowcount;

        if usertablecheck == 0:
            mycursor.execute("CREATE TABLE user (Name varchar(200), Role varchar(200));")
            mydb.commit()
        mycursor.execute("INSERT INTO user VALUES ('" + str(user) + "', '" + str(roletype) + "');")
        mydb.commit()
        mycursor.close()
        mydb.close()

        return redirect('home')


    return render(requests, 'registeruser.html')

def admin(request):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd='password',  # "mypassword",
        auth_plugin='mysql_native_password',
        database="university",
    )
    return HttpResponse("Hello Student")


def professors(request):
    return HttpResponse("Hello World")

def professors_search(request):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd='enter your password',  # "mypassword",
        auth_plugin='mysql_native_password',
        database="university",
    )

    mycursor = mydb.cursor()

    mycursor.execute('SELECT * FROM instructor WHERE current_salary>90000')

    data = '<table style="width:400px">'

    data += '</table>'

    mycursor.close()
    mydb.close()


def professors_salaries(request):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd='enter your password',  # "mypassword",
        auth_plugin='mysql_native_password',
        database="university",
    )

    mycursor = mydb.cursor()

    mycursor.execute('SELECT * FROM instructor WHERE current_salary>90000')

    data = '<table style="width:400px">'

    data += '</table>'

    mycursor.close()
    mydb.close()


def professors_studenst(request):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd='enter your password',  # "mypassword",
        auth_plugin='mysql_native_password',
        database="university",
    )

    mycursor = mydb.cursor()

    mycursor.execute('SELECT * FROM instructor WHERE current_salary>90000')

    data = '<table style="width:400px">'

    data += '</table>'

    mycursor.close()
    mydb.close()
