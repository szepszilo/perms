import webbrowser
import requests
import win32api
import threading
from tkinter import *
from PIL import Image,ImageTk
import sqlite3
# import imp
from tkinter import ttk, messagebox

import mysql.connector
from mysql.connector import Error
from ttkthemes import ThemedTk
__version__ = '1.0'
_AppName_ = 'Permissions'
__Owner__ = "Szép Szilveszter"
global conn, curs
data = None


defaultperm= "member"

def loginform():

    global login
    login = Tk()
    login.title(data.lang_Login)
    login.geometry("300x200")
    login.configure(background="#d3d5d2", height=300, width=400)
    login.resizable(False, False)

    Label(login, text=data.lang_Login, font="{Arial} 15 {bold}", foreground="#000000", background="#d3d5d2").place(anchor="nw", rely=0.05, relx=0.03, x=0, y=0)
    Label(login, background="#d3d5d2", font="{arial} 12 {}", text=data.lang_Username).place(anchor="nw", relx=0.05, rely=0.25, x=0, y=0)
    username = Entry (login)
    username.place(anchor="nw", relx=0.50, rely=0.259, x=0, y=0)

    Label(login, background="#d3d5d2", font="{arial} 12 {}", text=data.lang_Password).place(anchor="nw", relx=0.05, rely=0.45, x=0, y=0)
    password = Entry (login, show= "*")
    password.place(anchor="nw", relx=0.50, rely=0.459, x=0, y=0)

    Button(login, background="#c6e1e1", font="{arial} 10 {}", text=data.lang_Login ,command=lambda:logindata(username,password)).place(anchor="nw", relwidth=0.31, relx=0.50, rely=0.65, x=0, y=0)


    Button(login, background="#c6e1e1", font="{arial} 10 {}", text=data.lang_Signin,
           command= regPage).place(anchor="nw", relwidth=0.31,relx=0.10, rely=0.65, x=0, y=0)

    login.mainloop()


def regform():

    global register
    register = Tk()

    register.title(data.lang_Signin)
    register.geometry("300x400")
    register.configure(background="#d3d5d2", height=300, width=400)
    register.resizable(False, False)

    Label(register, text=data.lang_Login, font="{Arial} 15 {bold}", foreground="#000000", background="#d3d5d2").place(anchor="nw", rely=0.05, relx=0.03, x=0, y=0)
    Label(register, background="#d3d5d2", font="{arial} 12 {}", text=data.lang_Username).place(anchor="nw", relx=0.05,
                                                                                        rely=0.25, x=0, y=0)
    username = Entry(register)
    username.place(anchor="nw", relx=0.50, rely=0.259, x=0, y=0)

    Label(register, background="#d3d5d2", font="{arial} 12 {}", text=data.lang_Password).place(anchor="nw", relx=0.05,
                                                                                       rely=0.40, x=0, y=0)
    password = Entry(register, show="*")
    password.place(anchor="nw", relx=0.50, rely=0.409, x=0, y=0)

    Label(register, background="#d3d5d2", font="{arial} 12 {}", text=data.lang_Email).place(anchor="nw", relx=0.05,
                                                                                            rely=0.55, x=0, y=0)
    email = Entry(register)
    email.place(anchor="nw", relx=0.50, rely=0.559, x=0, y=0)

    Label(register, background="#d3d5d2", font="{arial} 12 {}", text=data.lang_Permission).place(anchor="nw", relx=0.05, rely=0.70,
                                                                                    x=0, y=0)
    permission  = Entry(register, state=DISABLED)
    permission.place(anchor="nw", relx=0.50, rely=0.709, x=0, y=0)
    permission.insert(0, data.lang_Member)

    Button(register, background="#c6e1e1", font="{arial} 10 {}", text=data.lang_Register ,command=lambda:db_insertLocal(username,password,email,permission)).place(anchor="nw", relwidth=0.31, relx=0.50, rely=0.85, x=0, y=0)

    Button(register, background="#c6e1e1", font="{arial} 10 {}", text=data.lang_Login,
           command= loginPage).place(anchor="nw", relwidth=0.31,relx=0.10, rely=0.85, x=0, y=0)

    register.mainloop()


def regPage():
    login.destroy()
    regform()

    
def loginPage():
    register.destroy()
    loginform()

    
def db_create():
    global conn, curs
    conn = sqlite3.connect("data/data.db")
    curs = conn.cursor()
    curs.execute("CREATE TABLE IF NOT EXISTS users (user TEXT, password TEXT, email TEXT, permission TEXT)")
    print ("Sikeres csatlakozás a helyi adatbázishoz")
    

def db_insertLocal(user, password, email, permission):
    if not user.get() or not password.get() or not email.get():
        error=Tk()
        error.title("error")
        error.resizable(False, False)
        error.geometry('200x50')
        error.configure(background="#d3d5d2", height=200, width=50)
        Label(error, background="#d3d5d2",
              text=data.lang_errorMiss).pack()

        return
    curs.execute("INSERT INTO users VALUES (?,?, ?, ?)", (user.get(), password.get(),
                                                                       email.get(), defaultperm))
    conn.commit()
    loginPage()


def logindata(username, password):
    global username1, password1
    if not username.get() or not password.get():
        error=Tk()
        error.title("error")
        error.resizable(False, False)
        error.geometry('200x50')
        error.configure(background="#d3d5d2", height=200, width=50)
        Label(error, background="#d3d5d2",
              text=data.lang_errorMiss).pack()

        return

    username = username.get()
    password = password.get()
    username1 = username
    password1 = password
    statement = f"SELECT user from users WHERE user='{username}' AND password = '{password}';"
    curs.execute(statement)
    if not curs.fetchone():  # An empty result evaluates to False.
        error = Tk()
        error.title("error")
        error.resizable(False, False)
        error.geometry('200x50')
        error.configure(background="#d3d5d2", height=200, width=50)
        Label(error, background="#d3d5d2",
              text=data.lang_errorLoginData).pack()

        return
    else:
        loginsucces(username, password)
        print(data.lang_Welcome +" "+ perms)


def loginsucces(username, password):
    global perms, permission1, emailaddress1
    permiss = f"SELECT permission from users WHERE user='{username}' AND password = '{password}';"
    curs.execute(permiss)
    perm = curs.fetchone()
    permission1 = perm[0]
    emailaddress = f"SELECT email from users WHERE user='{username}' AND password = '{password}';"
    curs.execute(emailaddress)
    emaila = curs.fetchone()
    emailaddress1 = emaila[0]
    if permission1 == "admin":
        perms = data.lang_Admin
        adminform()
    if permission1 == "member":
        perms = data.lang_Member
        memberform()


def adminform():
    login.destroy()
    global adminwindow
    adminwindow = Tk()

    adminwindow.title(data.lang_Administration)
    adminwindow.geometry("500x300")
    adminwindow.configure(background="#d3d5d2", height=300, width=400)
    adminwindow.resizable(False, False)

    Button(adminwindow, background="#c6e1e1", font="{arial} 10 {}", text=data.lang_NewUser,
           command=newuser_admin).place(anchor="nw", relwidth=0.30, relx=0.10, rely=0.20, x=0, y=0)

    Button(adminwindow, background="#c6e1e1", font="{arial} 10 {}", text=data.lang_UserPerms,
           command=userperms).place(anchor="nw", relwidth=0.30,relx=0.10, rely=0.35, x=0, y=0)

    Button(adminwindow, background="#c6e1e1", font="{arial} 10 {}", text=data.lang_Users,
           command=userperms).place(anchor="nw", relwidth=0.30,relx=0.10, rely=0.50, x=0, y=0)

    Button(adminwindow, background="#c6e1e1", font="{arial} 10 {}", text=data.lang_Logout,
           command=userperms).place(anchor="nw", relwidth=0.30,relx=0.10, rely=0.65, x=0, y=0)


    Label(adminwindow, background="#d3d5d2", font="{arial} 12 {}", text=data.lang_Administration).place(anchor="nw", relx=0.15,
                                                                                       rely=0.05, x=0, y=0)

    Label(adminwindow, background="#d3d5d2", font="{arial} 12 {}", text=data.lang_UserDatas).place(anchor="nw", relx=0.55,
                                                                                       rely=0.05, x=0, y=0)

    UserDatas = Frame(adminwindow, background="#C0C0C0", height=160, width=250).place(anchor="nw",relx=0.45, rely=0.20, x=0, y=0)

    Label(adminwindow, background="#C0C0C0", font="{arial} 12 {}", text=data.lang_Username+": "+username1).place(anchor="nw", relx=0.46,
                                                                                       rely=0.25, x=0, y=0)

    Label(adminwindow, background="#C0C0C0", font="{arial} 12 {}", text=data.lang_Email+": "+emailaddress1).place(anchor="nw", relx=0.46,
                                                                                       rely=0.40, x=0, y=0)

    Label(adminwindow, background="#C0C0C0", font="{arial} 12 {}", text=data.lang_Permission+": "+permission1).place(anchor="nw", relx=0.46,
                                                                                       rely=0.55, x=0, y=0)

    adminwindow.mainloop()


def memberform():
    login.destroy()
    global adminwindow
    adminwindow = Tk()

    adminwindow.title(data.lang_MemberWindow)
    adminwindow.geometry("500x300")
    adminwindow.configure(background="#d3d5d2", height=300, width=400)
    adminwindow.resizable(False, False)

    Button(adminwindow, background="#c6e1e1", font="{arial} 10 {}", text=data.lang_PassChange,
           command=newuser_admin).place(anchor="nw", relwidth=0.30, relx=0.10, rely=0.20, x=0, y=0)

    Button(adminwindow, background="#c6e1e1", font="{arial} 10 {}", text=data.lang_EmailChange,
           command=userperms).place(anchor="nw", relwidth=0.30,relx=0.10, rely=0.35, x=0, y=0)

    Button(adminwindow, background="#c6e1e1", font="{arial} 10 {}", text=data.lang_Users,
           command=userperms).place(anchor="nw", relwidth=0.30,relx=0.10, rely=0.50, x=0, y=0)

    Button(adminwindow, background="#c6e1e1", font="{arial} 10 {}", text=data.lang_Logout,
           command=userperms).place(anchor="nw", relwidth=0.30,relx=0.10, rely=0.65, x=0, y=0)


    Label(adminwindow, background="#d3d5d2", font="{arial} 12 {}", text=data.lang_MemberWindow).place(anchor="nw", relx=0.15,
                                                                                       rely=0.05, x=0, y=0)

    Label(adminwindow, background="#d3d5d2", font="{arial} 12 {}", text=data.lang_UserDatas).place(anchor="nw", relx=0.55,
                                                                                       rely=0.05, x=0, y=0)

    UserDatas = Frame(adminwindow, background="#C0C0C0", height=160, width=250).place(anchor="nw",relx=0.45, rely=0.20, x=0, y=0)

    Label(adminwindow, background="#C0C0C0", font="{arial} 12 {}", text=data.lang_Username+": "+username1).place(anchor="nw", relx=0.46,
                                                                                       rely=0.25, x=0, y=0)

    Label(adminwindow, background="#C0C0C0", font="{arial} 12 {}", text=data.lang_Email+": "+emailaddress1).place(anchor="nw", relx=0.46,
                                                                                       rely=0.40, x=0, y=0)

    Label(adminwindow, background="#C0C0C0", font="{arial} 12 {}", text=data.lang_Permission+": "+permission1).place(anchor="nw", relx=0.46,
                                                                                       rely=0.55, x=0, y=0)

    adminwindow.mainloop()

def userperms():
    pass

def newuser_admin():
    pass

def english():
    lang.destroy()
    langen()
    loginform()


def hungarian():
    lang.destroy()
    langhu()
    loginform()


def langform():
    global lang, language
    lang = Tk()
    lang.title("Languages")
    lang.geometry("300x100")
    lang.configure(background="#d3d5d2", height=300, width=400)
    lang.resizable(False, False)

    Button(lang, background="#c6e1e1", font="{arial} 10 {}", text="Magyar" ,command=lambda:hungarian()).place(anchor="nw", relwidth=0.50, relheight=1, relx=0.50, rely=0, x=0, y=0)
    Button(lang, background="#c6e1e1", font="{arial} 10 {}", text="English" ,command=lambda: english()).place(anchor="nw", relwidth=0.50, relheight=1, relx=0.0, rely=0, x=0, y=0)


    lang.mainloop()


def getVarFromFile(filename, langpack):
    import imp
    f = open(filename)
    global data
    data = imp.load_source('data', langpack, f)
    print(data.lang_Welcome)
    f.close()


def langen():
    getVarFromFile("data/en-US.txt", "data/en-US.txt")


def langhu():
    getVarFromFile("data/hu-HU.txt", "data/hu-HU.txt")




db_create()
langform()


