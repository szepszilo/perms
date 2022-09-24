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
__version__ = '1.1'
__AppName__ = 'Permissions'
__Owner__ = "Szép Szilveszter"
global conn, curs
data = None


defaultperm= "member"

#### FRONT #### FRONT #### FRONT #### FRONT #### FRONT #### FRONT #### FRONT ####

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

    Button(login, background="#c6e1e1", font="{arial} 10 {}", text=data.lang_About,
           command= about).place(anchor="nw", relwidth=0.31,relx=0.50, rely=0.10, x=0, y=0)

    login.mainloop()
def regform():

    global register
    register = Tk()

    register.title(data.lang_Signin)
    register.geometry("300x400")
    register.configure(background="#d3d5d2", height=300, width=400)
    register.resizable(False, False)

    Label(register, text=data.lang_Signin, font="{Arial} 15 {bold}", foreground="#000000", background="#d3d5d2").place(anchor="nw", rely=0.05, relx=0.03, x=0, y=0)
    Label(register, background="#d3d5d2", font="{arial} 12 {}", text=data.lang_Username+":").place(anchor="nw", relx=0.05,
                                                                                        rely=0.25, x=0, y=0)
    username = Entry(register)
    username.place(anchor="nw", relx=0.50, rely=0.259, x=0, y=0)

    Label(register, background="#d3d5d2", font="{arial} 12 {}", text=data.lang_Password+":").place(anchor="nw", relx=0.05,
                                                                                       rely=0.40, x=0, y=0)
    password = Entry(register, show="*")
    password.place(anchor="nw", relx=0.50, rely=0.409, x=0, y=0)

    Label(register, background="#d3d5d2", font="{arial} 12 {}", text=data.lang_Email+":").place(anchor="nw", relx=0.05,
                                                                                            rely=0.55, x=0, y=0)
    email = Entry(register)
    email.place(anchor="nw", relx=0.50, rely=0.559, x=0, y=0)

    Label(register, background="#d3d5d2", font="{arial} 12 {}", text=data.lang_Permission+":").place(anchor="nw", relx=0.05, rely=0.70,
                                                                                    x=0, y=0)
    permission = StringVar(register)
    permission.set(data.lang_Permission)
    permissions = OptionMenu(register, permission, data.lang_Member,data.lang_Admin)
    permissions.place(anchor="nw", relx=0.50, rely=0.70, x=0, y=0)

    Button(register, background="#c6e1e1", font="{arial} 10 {}", text=data.lang_Register ,command=lambda:db_insertLocal(username,password,email,permission)).place(anchor="nw", relwidth=0.31, relx=0.50, rely=0.85, x=0, y=0)

    Button(register, background="#c6e1e1", font="{arial} 10 {}", text=data.lang_Login,
           command= loginPage).place(anchor="nw", relwidth=0.31,relx=0.10, rely=0.85, x=0, y=0)

    register.mainloop()

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

def adminform():
    login.destroy()
    global adminwindow
    adminwindow = Tk()

    adminwindow.title(data.lang_Administration)
    adminwindow.geometry("500x300")
    adminwindow.configure(background="#d3d5d2", height=300, width=400)
    adminwindow.resizable(False, False)

    Button(adminwindow, background="#c6e1e1", font="{arial} 10 {}", text=data.lang_NewUser,
           command=newuser_adminform).place(anchor="nw", relwidth=0.30, relx=0.10, rely=0.20, x=0, y=0)

    Button(adminwindow, background="#c6e1e1", font="{arial} 10 {}", text=data.lang_UserPerms,
           command=userpermsform).place(anchor="nw", relwidth=0.30,relx=0.10, rely=0.35, x=0, y=0)

    Button(adminwindow, background="#c6e1e1", font="{arial} 10 {}", text=data.lang_Users,
           command=users_manageform).place(anchor="nw", relwidth=0.30,relx=0.10, rely=0.50, x=0, y=0)

    Button(adminwindow, background="#c6e1e1", font="{arial} 10 {}", text=data.lang_Logout,
           command=logout).place(anchor="nw", relwidth=0.30,relx=0.10, rely=0.65, x=0, y=0)


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

    Label(adminwindow, background="#d3d5d2", font="{arial} 24 {}", text="Beta ver.: "+__version__).place(anchor="nw",
                                                                                                        relx=0.15, rely=0.80, x=0, y=0)

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
           command=Password_change).place(anchor="nw", relwidth=0.30, relx=0.10, rely=0.20, x=0, y=0)

    Button(adminwindow, background="#c6e1e1", font="{arial} 10 {}", text=data.lang_EmailChange,
           command=Email_change).place(anchor="nw", relwidth=0.30,relx=0.10, rely=0.35, x=0, y=0)

    Button(adminwindow, background="#c6e1e1", font="{arial} 10 {}", text=data.lang_Users,
           command=users_manageform).place(anchor="nw", relwidth=0.30,relx=0.10, rely=0.50, x=0, y=0)

    Button(adminwindow, background="#c6e1e1", font="{arial} 10 {}", text=data.lang_Logout,
           command=logout).place(anchor="nw", relwidth=0.30,relx=0.10, rely=0.65, x=0, y=0)


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


def userpermsform():
    pass

def newuser_adminform():
    registerfromadmin = Toplevel(adminwindow)

    registerfromadmin.title(data.lang_Signin)
    registerfromadmin.geometry("300x400")
    registerfromadmin.configure(background="#d3d5d2", height=300, width=400)
    registerfromadmin.resizable(False, False)

    Label(registerfromadmin, text=data.lang_Login, font="{Arial} 15 {bold}", foreground="#000000", background="#d3d5d2").place(anchor="nw", rely=0.05, relx=0.03, x=0, y=0)
    Label(registerfromadmin, background="#d3d5d2", font="{arial} 12 {}", text=data.lang_Username+":").place(anchor="nw", relx=0.05,
                                                                                        rely=0.25, x=0, y=0)
    username = Entry(registerfromadmin)
    username.place(anchor="nw", relx=0.50, rely=0.259, x=0, y=0)

    Label(registerfromadmin, background="#d3d5d2", font="{arial} 12 {}", text=data.lang_Password+":").place(anchor="nw", relx=0.05,
                                                                                       rely=0.40, x=0, y=0)
    password = Entry(registerfromadmin, show="*")
    password.place(anchor="nw", relx=0.50, rely=0.409, x=0, y=0)

    Label(registerfromadmin, background="#d3d5d2", font="{arial} 12 {}", text=data.lang_Email+":").place(anchor="nw", relx=0.05,
                                                                                            rely=0.55, x=0, y=0)
    email = Entry(registerfromadmin)
    email.place(anchor="nw", relx=0.50, rely=0.559, x=0, y=0)

    Label(registerfromadmin, background="#d3d5d2", font="{arial} 12 {}", text=data.lang_Permission+":").place(anchor="nw", relx=0.05, rely=0.70,
                                                                                            x=0, y=0)
    permission = StringVar(registerfromadmin)
    permission.set(data.lang_Permission)
    permissions = OptionMenu(registerfromadmin, permission, data.lang_Member,data.lang_Admin)
    permissions.place(anchor="nw", relx=0.50, rely=0.70, x=0, y=0)

    Button(registerfromadmin, background="#c6e1e1", font="{arial} 10 {}", text=data.lang_Register ,command=lambda:db_insertLocal(username,password,email,permission)).place(anchor="nw", relwidth=0.31, relx=0.50, rely=0.85, x=0, y=0)

    Button(registerfromadmin, background="#c6e1e1", font="{arial} 10 {}", text=data.lang_Login,
           command= loginPage).place(anchor="nw", relwidth=0.31,relx=0.10, rely=0.85, x=0, y=0)

    registerfromadmin.mainloop()
def users_manageform():
    usertable = Toplevel(adminwindow)
    usertable.title(data.lang_managingusers)
    usertable.geometry('800x270')
    usertable.configure(background="#d3d5d2", height=800, width=270)

    Button(usertable, background="#c6e1e1", font="{arial} 10 {}", text=data.lang_Query, command=lambda:db_query(table)).place(anchor="nw",relwidth=0.15,relx=0.05, rely=0.86,x=0, y=0)
    cols = (data.lang_Username, data.lang_Password, data.lang_Email, data.lang_Permission)
    table = ttk.Treeview(usertable, columns=cols, show="headings")
    for col in cols:
        table.heading(col, text=col)
    table.place(anchor="nw",relwidth=1,relx=0.0, rely=0.0,x=0, y=0)
    usertable.resizable(False, False)

    if permission1 == "admin":
        Label(usertable, background="#d3d5d2", font="{arial} 16 {}", text=data.lang_deluser+": ").place(
            anchor="nw",
            relx=0.40, rely=0.86, x=0, y=0)
        deluserentry = Entry(usertable, font="{arial} 12 {}")
        deluserentry.place(anchor="nw", relx=0.55, rely=0.865, x=0, y=0, relheight=0.1)
        Button(usertable, background="#c6e1e1", font="{arial} 10 {}", text=data.lang_delete,
               command=lambda:delete_person(deluserentry) and db_query(table)).place(anchor="nw", relwidth=0.15, relx=0.80, rely=0.86, x=0, y=0)
        deluserentry.delete(0, 'end')

def about():
    about = Toplevel(login)
    about.geometry('200x100')
    about.title(data.lang_About)
    about.resizable(False, False)
    about.configure(background="#d3d5d2", height=200, width=200)
    Label(about,background="#d3d5d2", text=data.lang_CreatedBy + "Szép Szilveszter\n" + __AppName__ + __version__ + "\n" + data.lang_Email + ": szep.code@gmail.com").pack()
    Button(about, background="#c6e1e1", font="{arial} 10 {}", text=data.lang_CheckUpdate, command=check_updates).place(anchor="nw", relwidth=0.60, relx=0.20, rely=0.60, x=0, y=0)
#### FRONT #### FRONT #### FRONT #### FRONT #### FRONT #### FRONT #### FRONT ####

#### BACK #### BACK #### BACK #### BACK #### BACK #### BACK #### BACK #### BACK ####
def db_create():
    global conn, curs
    conn = sqlite3.connect("data/data.db")
    curs = conn.cursor()
    curs.execute("CREATE TABLE IF NOT EXISTS users (user TEXT, password TEXT, email TEXT, permission TEXT)")
    print ("Sikeres csatlakozás a helyi adatbázishoz")

def regPage():
    login.destroy()
    regform()
def loginPage():
    register.destroy()
    loginform()

def db_insertLocal(user, password, email, permission):
    if permission.get() == data.lang_Admin:
        permissions = "admin"
    if permission.get() == data.lang_Member:
        permissions = "member"
    if not user.get() or not password.get() or not email.get():
        error=Tk()
        error.title(data.lang_Error)
        error.resizable(False, False)
        error.geometry('200x50')
        error.configure(background="#d3d5d2", height=200, width=50)
        Label(error, background="#d3d5d2",
              text=data.lang_errorMiss).pack()

        return
    curs.execute("INSERT INTO users VALUES (?,?, ?, ?)", (user.get(), password.get(),
                                                                       email.get(), permissions))
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

def english():
    lang.destroy()
    langen()
    loginform()
def hungarian():
    lang.destroy()
    langhu()
    loginform()


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

def logout():
    pass
def Password_change():
    pass
def Email_change():
    pass
def db_query(table):
    curs.execute("SELECT * FROM users")
    datas = curs.fetchall()
    table.delete(*table.get_children())
    rowid = 1
    for data in datas:
        table.insert("", "end", values=(data[0],data[1],data[2],data[3]))
        rowid += 1

def delete_person(deluserentry):

    if not deluserentry.get():
        error2=Tk()
        error2.title(data.lang_Error)
        error2.resizable(False, False)
        error2.iconbitmap("servers.ico")
        error2.geometry('200x50')
        error2.configure(background="#d3d5d2", height=200, width=50)
        Label(error2, background="#d3d5d2",
              text=data.lang_ErrorMissUsername).pack()
    else:
        del_user_id=str(deluserentry.get())
        print (del_user_id)
        print (type(del_user_id))
        deletecomm="DELETE FROM users WHERE user = (?) "
        curs.execute(deletecomm, (del_user_id,))
        conn.commit()

def check_updates():
    try:
        response = requests.get(
            'https://raw.githubusercontent.com/szepszilo/database/main/version.txt')
        verdatas = response.text

        if float(verdatas) > float(__version__):
            messagebox.showinfo(data.lang_SoftwareUpdate, data.lang_NewUpdateAvailable)
            mb1 = messagebox.askyesno(data.lang_Update, f'{data.lang_AvailableVersion} {__AppName__} {__version__}{data.lang_AvailableVersionFORHU}\n{data.lang_Version} {verdatas}')
            if mb1 is True:
                # -- Replace the url for your file online with the one below.
                # webbrowser.open_new_tab('https://raw.githubusercontent.com/szepszilo/database/main/'
                #                         'update.msi?raw=true')
                webbrowser.open_new_tab('https://github.com/szepszilo/database/')

                #parent.destroy()
            else:
                pass
        else:
            messagebox.showinfo(data.lang_SoftwareUpdate, data.lang_NoUpdateAvailable)
    except Exception as e:
        messagebox.showinfo(data.lang_SoftwareUpdate, data.lang_UpdateError + str(e))
db_create()
langform()


