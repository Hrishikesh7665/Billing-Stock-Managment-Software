from tkinter import *
from tkinter import messagebox, ttk, font
import os, sys
import sqlite3
Secret_key = "Secrect Key"



Login_suc = False



def resource_path():
    CurrentPath = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    # Look for the 'sprites' folder on the path I just gave you:
    spriteFolderPath = os.path.join(CurrentPath, 'Assets/')
    path = os.path.join(spriteFolderPath)
    newPath = path.replace(os.sep, '/')
    return newPath

_path = resource_path()




#Generate A Folder In APP DATA Folder
app_Data = (os.getenv('APPDATA'))+"\BillingSoftwareByHrishikesh\\"
userAccount_DB = app_Data+"USERDATABASE.db"


#check for APP data Folder IF Exits:

if not os.path.exists(app_Data):
    os.makedirs(app_Data)



#Login Window

background = "white"    #Main BG Color


loginwindow = Tk()
loginwindow.title("User Login")

loginwindow.config(bg=background)
loginwindow.resizable(False,False)


secret_code = StringVar(loginwindow)
secret_code.set(Secret_key)
User_name_VAR = StringVar(loginwindow)
User_pass_VAR = StringVar(loginwindow)
svar = StringVar(loginwindow)
rememberV =IntVar(loginwindow)
Check_Box1 = IntVar(loginwindow)
Check_Box2 = IntVar(loginwindow)
deli = 150
#open tkinter window center of screen

def center_window(w,h):
    # get screen width and height
    ws = loginwindow.winfo_screenwidth()
    hs = loginwindow.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)      #hs/2 is for proper center window
    loginwindow.geometry('%dx%d+%d+%d' % (w, h, x, y))

center_window(380, 380)





eye_close = PhotoImage(file=_path+"eye_close.png")
eye_open = PhotoImage(file=_path+"eye_open.png")
logo = PhotoImage(file = _path+'LOGO.png')
titlebar_icon = _path+"user_icon.ico"
sus = PhotoImage(file = _path+'sus.png')
logo = logo.subsample(14,14)                #





def login_SC():
    global Login_suc
    conn = sqlite3.connect(userAccount_DB)
    cursor = conn.execute("SELECT NAME, PASSWORD, Remember from Users")
    rows= cursor.fetchall()
    U_name = (rows[0][0])
    U_pass = (rows[0][1])
    rem = int(rows[0][2])
    conn.close()
    User_name_VAR.set(U_name)
    if rem ==0:
        User_pass_VAR.set("")
    elif rem ==1:
        User_pass_VAR.set(U_pass)
    rememberV.set(rem)
    for i in loginwindow.winfo_children():
        i.destroy()
    def Login_Btn_fun ():
        global Login_suc
        if User_pass_VAR.get ()=="":
            Label(loginwindow,text="(Please Enter Password)",font=("Arial Black",9),bg="white",fg="indianred1").place(x=100,y=330)
        elif User_pass_VAR.get ()!= U_pass:
            a = messagebox.askretrycancel("Password Error", "Wrong Password Try Again?")
            if a!=True:
                loginwindow.destroy()
                sys.exit()
            else:
                User_pass_VAR.set("")
        else:
            conn = sqlite3.connect(userAccount_DB)
            conn.execute("""UPDATE Users SET
                    Remember = :Rem
                    WHERE NAME = :name""",{'name' : U_name,
                                            'Rem' : int(rememberV.get())})
            conn.commit()
            conn.close()
            Login_suc = True
            loginwindow.destroy()

    def set_N_Pass():
        for i in loginwindow.winfo_children():
            i.destroy()
        secret_code.set("")

        def save_New_pass():
            if secret_code.get() =="":
                lb.config(text="Password Field Can't Be Blank")
            else:
                for i in loginwindow.winfo_children():
                    i.destroy()
                conn = sqlite3.connect(userAccount_DB)
                conn.execute("""UPDATE Users SET
                        PASSWORD = :pass,
                        Remember = :Rem
                        WHERE NAME = :name""",{'name'  : U_name,
                                                'pass' : secret_code.get(),
                                                'Rem'  : 0})
                conn.commit()
                conn.close()
                Label(loginwindow,text="\n",bg=background,fg=background,font=("Copperplate Gothic Bold",8)).pack()
                Label(loginwindow,image=sus,background=background).pack()
                Label(loginwindow,text="Successful\n",bg=background,font=("Copperplate Gothic Bold",17)).pack()
                Label(loginwindow,text=("Dear, "+User_name_VAR.get()+"\nYour Password Changed Successfully\n\nPlease Go To Login Page\n& Login With Your New Password"),bg=background,font=("Bookman Old Style",13,"italic")).pack()
                Label(loginwindow,text="\n",bg=background,fg=background,font=("Copperplate Gothic Bold",8)).pack()
                Button(loginwindow, text='   Login    ', bd=0, font=('Arial 12'), fg='white', bg='#00CCCC',command=login_SC,relief=FLAT).pack()

        canvas = Canvas(loginwindow,relief='ridge',highlightthickness =0,height=60,bg=background)
        Label(canvas,text="Create New Password",font=("Bahnschrift",14),bg=background).place(x=92,y=0)
        canvas.create_line(90, 35, 290, 35)
        Label(loginwindow,text="  ",bg=background,fg=background,font=("Book Antiqua",7)).pack()
        canvas.pack()
        Label(loginwindow,text="  ",bg=background,fg=background,font=("Copperplate Gothic Bold",14)).pack()
        Label(loginwindow,text="Enter New Password",bg=background,font=("Copperplate Gothic Bold",17)).pack()
        Label(loginwindow,text="\n",bg=background,fg=background,font=("Copperplate Gothic Bold",10)).pack()
        UserpassEntry4 = Entry(loginwindow,textvariable=secret_code,bg="seashell2",font=("Bahnschrift",15),show="*",justify=CENTER,width=25)
        UserpassEntry4.pack()
        Label(loginwindow,text="  ",bg=background,fg=background,font=("Copperplate Gothic Bold",15)).pack()
        Button(loginwindow, text='   Submit   ', bd=0, font=('Arial 12'), fg='white', bg='#14A769',command=save_New_pass,relief=FLAT).pack()
        Label(loginwindow,text="            ",bg=background,fg=background,font=("Copperplate Gothic Bold",6)).pack()
        lb = Label(loginwindow,text="",font=("Arial Black",9),bg="white",fg="indianred1")
        lb.pack()
        def function_eye_open_button4 ():
            UserpassEntry4.config(show="")
            eye_close_button4.place(x=304,y=175)
            eye_open_button4.place(x=1000,y=1000)

        def function_eye_close_button4 ():
            UserpassEntry4.config(show="*")
            eye_close_button4.place(x=1000,y=1000)
            eye_open_button4.place(x=304,y=175)
        eye_open_button4 = Button(loginwindow, image=eye_open,activebackground="#c0c0c0",bd=0,bg="#c0c0c0",cursor="hand2",command=function_eye_open_button4)
        eye_open_button4.place(x=304,y=175)
        eye_close_button4 = Button(loginwindow, image=eye_close, bd=0,activebackground="#c0c0c0",bg="#c0c0c0",cursor="hand2",command=function_eye_close_button4)

    def forget_Pass():
        for i in loginwindow.winfo_children():
            i.destroy()
        svar.set("")
        #secret_code.set("")
        canvas = Canvas(loginwindow,relief='ridge',highlightthickness =0,height=60,bg=background)
        Label(canvas,text="Change or Reset Password",font=("Bahnschrift",14),bg=background).place(x=75,y=0)
        canvas.create_line(80, 35, 308, 35)
        Label(loginwindow,text="  ",bg=background,fg=background,font=("Book Antiqua",7)).pack()
        canvas.pack()
        first_Frame = Frame (loginwindow,bg=background)
        def CH_Selected (e):
            secret_code.set("")
            if e == 1:
                def submit_B_Fun():
                    if secret_code.get() == "":
                        lb.config(text="(Please Enter Secrect Key)")
                    elif secret_code.get() == Secret_key:
                        set_N_Pass()
                    elif secret_code.get() != Secret_key:
                        a = messagebox.askretrycancel("Error", "Wrong Secret key Try Again?")
                        if a!=True:
                            loginwindow.destroy()
                            sys.exit()
                        else:
                            secret_code.set("")
                if Check_Box1.get() == 1:
                    Ch_B2.config(state=DISABLED)
                    Check_Box2.set(0)
                    for i in first_Frame.winfo_children():
                        i.destroy()
                first_Frame.pack()
                Label(first_Frame,text="  ",bg=background,fg=background,font=("Copperplate Gothic Bold",14)).pack()
                Label(first_Frame,text="Enter Secret Code",bg=background,font=("Copperplate Gothic Bold",17)).pack()
                Label(first_Frame,text="(Read My GitHub Repo Info For Key)",bg=background,font=("Cooper Black",10)).pack()
                Label(first_Frame,text="  ",bg=background,fg=background,font=("Copperplate Gothic Bold",10)).pack()
                Entry(first_Frame,textvariable=secret_code,bg="seashell2",font=("Eras Bold ITC",14),show="*",width=25).pack()
                Label(first_Frame,text="  ",bg=background,fg=background,font=("Copperplate Gothic Bold",15)).pack()
                Button(first_Frame, text='   Submit   ', bd=0, font=('Arial 12'), fg='white', bg='#14A769', command=submit_B_Fun, relief=FLAT).pack()
                Label(first_Frame,text="            ",bg=background,fg=background,font=("Copperplate Gothic Bold",6)).pack()
                lb = Label(first_Frame,text="",font=("Arial Black",9),bg="white",fg="indianred1")
                lb.pack()
                if Check_Box1.get() == 0:
                    Ch_B2.config(state=NORMAL)
                    Check_Box2.set(0)
                    for i in first_Frame.winfo_children():
                        i.destroy()

            elif e == 2:
                def submit_B2_Fun():
                    if secret_code.get() == "":
                        lb.config(text="(Please Enter Old Password)")
                    elif secret_code.get() == U_pass:
                        set_N_Pass()
                    elif secret_code.get() != U_pass:
                        a = messagebox.askretrycancel("Error", "Wrong Old Password Try Again?")
                        if a!=True:
                            loginwindow.destroy()
                            sys.exit()
                        else:
                            secret_code.set("")

                if Check_Box2.get() == 1:
                    Ch_B1.config(state=DISABLED)
                    Check_Box1.set(0)
                    for i in first_Frame.winfo_children():
                        i.destroy()
                    first_Frame.pack()
                    Label(first_Frame,text="  ",bg=background,fg=background,font=("Copperplate Gothic Bold",14)).pack()
                    Label(first_Frame,text="Enter Old Password",bg=background,font=("Copperplate Gothic Bold",17)).pack()
                    Label(first_Frame,text="  ",bg=background,fg=background,font=("Copperplate Gothic Bold",10)).pack()
                    UserpassEntry3 = Entry(first_Frame,textvariable=secret_code,justify=CENTER,bg="seashell2",font=('Bahnschrift',15),show="*",width=25)
                    UserpassEntry3.pack()
                    Label(first_Frame,text="  ",bg=background,fg=background,font=("Copperplate Gothic Bold",15)).pack()
                    Button(first_Frame, text='   Submit   ', bd=0, font=('Arial 12'), fg='white', bg='#14A769', command=submit_B2_Fun, relief=FLAT).pack()
                    Label(first_Frame,text="            ",bg=background,fg=background,font=("Copperplate Gothic Bold",6)).pack()
                    lb = Label(first_Frame,text="",font=("Arial Black",9),bg="white",fg="indianred1")
                    lb.pack()
                def function_eye_open_button3 ():
                    UserpassEntry3.config(show="")
                    eye_close_button3.place(x=254,y=81)
                    eye_open_button3.place(x=1000,y=1000)

                def function_eye_close_button3 ():
                    UserpassEntry3.config(show="*")
                    eye_close_button3.place(x=1000,y=1000)
                    eye_open_button3.place(x=254,y=81)
                eye_open_button3 = Button(first_Frame, image=eye_open,activebackground="#c0c0c0",bd=0,bg="#c0c0c0",cursor="hand2",command=function_eye_open_button3)
                eye_open_button3.place(x=254,y=81)
                eye_close_button3 = Button(first_Frame, image=eye_close, bd=0,activebackground="#c0c0c0",bg="#c0c0c0",cursor="hand2",command=function_eye_close_button3)

                if Check_Box2.get() == 0:
                    Ch_B1.config(state=NORMAL)
                    Check_Box1.set(0)
                    for i in first_Frame.winfo_children():
                        i.destroy()


        Ch_B1 = Checkbutton(loginwindow,bg=background,activeforeground="blue",justify=CENTER,font=("Cantarell",11,"bold"),command=lambda:CH_Selected(1),text="Reset Password With Secrect Key",variable=Check_Box1,onvalue=1,offvalue=0)
        Ch_B1.pack()
        Ch_B2 = Checkbutton(loginwindow,bg=background,activeforeground="blue",justify=CENTER,font=("Cantarell",11,"bold"),command=lambda:CH_Selected(2),text="Change Password With Old Password",variable=Check_Box2,onvalue=1,offvalue=0)
        Ch_B2.pack()

        labl = Label(loginwindow,font=("ModernNo20",10), textvariable=svar, height=1,width=56 )
        def shif2():
            shif2.msg = shif2.msg[1:] + shif2.msg[0]
            svar.set(shif2.msg)
            loginwindow.after(deli, shif2)
        shif2.msg = '                     To know the secret key read this project GitHub repository.                  '
        shif2()
        labl.place(x=0,y=0)



    Label(loginwindow,image=logo,bg=background).pack()
    Label(loginwindow,text="Wellcome",font=("Segoe UI Semibold",20),bg=background).pack()
    Label(loginwindow,textvariable=User_name_VAR,font=("Segoe UI Semibold",25),bg=background).pack()
    Label(loginwindow,text="  ",font=("Segoe UI Semibold",5),fg=background,bg=background).pack()
    Label(loginwindow,text="     Password",font=("Book Antiqua",14),bg=background).pack(anchor=SW)
    UserpassEntry2 = Entry(loginwindow,justify='center',textvariable = User_pass_VAR,show="*",width=29,bg="#c0c0c0",font=('Bahnschrift',15),bd=2)
    Label(loginwindow,text="    ",font=("Book Antiqua",14),bg=background).pack(side=LEFT)
    UserpassEntry2.pack(anchor=NW)
    Label(loginwindow,text="\n \n",font=("Book Antiqua",24),bg=background).pack()
    Login_btn = Button(loginwindow,text="   Log In    ",font=('Bahnschrift',12),width = 35,bd=2,bg ="#fa2649",fg="white",command=Login_Btn_fun)
    Login_btn.place(x=25,y=291)
    forget_Btn = Button(loginwindow,text="Forget Password",cursor="hand2",font=('Book Antiqua',10),bd=0,activebackground=background, command=forget_Pass, bg =background,fg="blue")
    forget_Btn.place(x=247,y=248)
    def onhover(e):
        forget_Btn['fg'] = "red"
    def onleave(e):
        forget_Btn['fg'] = "blue"
    forget_Btn.bind('<Enter>', onhover)
    forget_Btn.bind('<Leave>', onleave)
    Checkbutton(loginwindow, font=('Book Antiqua',10), text = "Remember Me", variable = rememberV, onvalue = 1, offvalue = 0,bg=background,activebackground=background).place(x=21,y=248)
    def function_eye_open_button2 ():
        UserpassEntry2.config(show="")
        eye_close_button2.place(x=325,y=222)
        eye_open_button2.place(x=1000,y=1000)

    def function_eye_close_button2 ():
        UserpassEntry2.config(show="*")
        eye_close_button2.place(x=1000,y=1000)
        eye_open_button2.place(x=325,y=222)
    eye_open_button2 = Button(loginwindow, image=eye_open,activebackground="#c0c0c0",bd=0,bg="#c0c0c0",cursor="hand2",command=function_eye_open_button2)
    eye_open_button2.place(x=325,y=222)
    eye_close_button2 = Button(loginwindow, image=eye_close, bd=0,activebackground="#c0c0c0",bg="#c0c0c0",cursor="hand2",command=function_eye_close_button2)



def create_AC():
    User_name_VAR.set("")
    User_pass_VAR.set("")
    for i in loginwindow.winfo_children():
        i.destroy()

    def Sus_SR ():
        for i in loginwindow.winfo_children():
            i.destroy()
        conn = sqlite3.connect(userAccount_DB)
        conn.execute('''CREATE TABLE Users
         (NAME          TEXT    PRIMARY KEY    NOT NULL,
         PASSWORD       TEXT    NOT NULL,
         Remember       INT);''')
        conn.execute("INSERT INTO Users (NAME, PASSWORD, Remember) values(?,?,?)",(User_name_VAR.get(), User_pass_VAR.get(), 0))
        conn.commit()
        conn.close()
        Label(loginwindow,text="\n",bg=background,fg=background,font=("Copperplate Gothic Bold",8)).pack()
        Label(loginwindow,image=sus,background=background).pack()
        Label(loginwindow,text="Successful\n",bg=background,font=("Copperplate Gothic Bold",17)).pack()
        Label(loginwindow,text=("Dear, "+User_name_VAR.get()+"\nYour Account Was Crated Successfully\n\nPlease Go To Login Page\n& Login With Your Password"),bg=background,font=("Bookman Old Style",13,"italic")).pack()
        Label(loginwindow,text="\n",bg=background,fg=background,font=("Copperplate Gothic Bold",8)).pack()
        Button(loginwindow, text='   Login    ', bd=0, font=('Arial 12'), fg='white', bg='#00CCCC',command=login_SC,relief=FLAT).pack()


    def CON_BN ():
        if User_name_VAR.get() == "" or User_pass_VAR.get() == "":
            messagebox.showerror("Invalid Field","Please Enter User Name & Password")
        else:
            for i in loginwindow.winfo_children():
                i.destroy()

            canvas = Canvas(loginwindow,relief='ridge',highlightthickness =0,height=60,bg=background)
            Label(canvas,text="Create New User Account",font=("Bahnschrift",14),bg=background).place(x=75,y=0)
            canvas.create_line(80, 35, 296, 35)
            Label(loginwindow,text="  ",bg=background,fg=background,font=("Book Antiqua",7)).pack()
            canvas.pack()
            Label(loginwindow,text="Create Account For",bg=background,font=("Copperplate Gothic Bold",17)).pack()
            Label(loginwindow,text=("\n"+User_name_VAR.get()+"\n"),bg=background,font=("Bookman Old Style",17,"bold")).pack()
            Label(loginwindow,text=" ",bg=background,fg=background,font=("Copperplate Gothic Bold",4)).pack()
            Button(loginwindow, text='   Yes   ', bd=0, font=('Arial 12'), fg='white', bg='#14A769',command=Sus_SR,relief=FLAT).pack()
            Label(loginwindow,text=" ",bg=background,fg=background,font=("Copperplate Gothic Bold",8)).pack()
            Button(loginwindow, text='   No    ', bd=0, font=('Arial 12'), fg='white', bg='#FF6666',command=create_AC,relief=FLAT).pack()


    canvas = Canvas(loginwindow,relief='ridge',highlightthickness =0,height=60,bg=background)
    Label(canvas,text="Create New User Account",font=("Bahnschrift",14),bg=background).place(x=75,y=0)
    canvas.create_line(80, 35, 296, 35)
    Label(loginwindow,text="  ",bg=background,fg=background,font=("Book Antiqua",7)).pack()
    canvas.pack()
    Label(loginwindow,text=" ",bg=background,fg=background,font=("Copperplate Gothic Bold",8)).pack()
    Label(loginwindow,text="        Enter New User Name",bg=background,font=("Book Antiqua",14)).pack(anchor=W)
    Entry(loginwindow,textvariable=User_name_VAR,bg="seashell2",font=("Arial Rounded MT Bold",14),justify=CENTER,width=27).pack()
    Label(loginwindow,text="  \n",bg=background,fg=background,font=("Copperplate Gothic Bold",17)).pack()
    Label(loginwindow,text="        Enter Password",bg=background,font=("Book Antiqua",14)).pack(anchor=W)
    UserpassEntry = Entry(loginwindow,textvariable=User_pass_VAR,bg="seashell2",font=('Bahnschrift',15),show="*",justify=CENTER,width=27)
    UserpassEntry.pack()
    Label(loginwindow,text="  ",bg=background,fg=background,font=("Copperplate Gothic Bold",17)).pack()
    Button(loginwindow, text='   Continue   ', bd=0, font=('Arial 12'), fg='white', bg='#14A769',command=CON_BN,relief=FLAT).pack()

    def function_eye_open_button ():
        UserpassEntry.config(show="")
        eye_close_button.place(x=315,y=240)
        eye_open_button.place(x=1000,y=1000)

    def function_eye_close_button ():
        UserpassEntry.config(show="*")
        eye_close_button.place(x=1000,y=1000)
        eye_open_button.place(x=315,y=240)
    eye_open_button = Button(loginwindow, image=eye_open,activebackground="#c0c0c0",bd=0,bg="#c0c0c0",cursor="hand2",command=function_eye_open_button)#,command=function_eye_open_button
    eye_open_button.place(x=315,y=240)
    eye_close_button = Button(loginwindow, image=eye_close, bd=0,activebackground="#c0c0c0",bg="#c0c0c0",cursor="hand2",command=function_eye_close_button)

def newuser():
    secret_code.set("")
    def ch():
        if secret_code.get() == "":
            lb.config(text="Please Enter Secrect Key")
        elif secret_code.get() == Secret_key:
            create_AC()
        elif secret_code.get() != Secret_key:
            a = messagebox.askretrycancel("Error", "Wrong Secret key Try Again?")
            if a!=True:
                loginwindow.destroy()
                sys.exit()
            else:
                secret_code.set("")
    Label(loginwindow,text="  \n        \n            \n",bg=background,fg=background,font=("Copperplate Gothic Bold",17)).pack()
    Label(loginwindow,text="Enter Secret Code",bg=background,font=("Copperplate Gothic Bold",17)).pack()
    Label(loginwindow,text="(Read My GitHub Repo Info For Key)",bg=background,font=("Cooper Black",10)).pack()
    Label(loginwindow,text="  ",bg=background,fg=background,font=("Copperplate Gothic Bold",10)).pack()
    Entry(loginwindow,textvariable=secret_code,bg="seashell2",font=("Eras Bold ITC",14),show="*",width=25).pack()
    Label(loginwindow,text="  ",bg=background,fg=background,font=("Copperplate Gothic Bold",15)).pack()
    Button(loginwindow, text='   Submit   ', bd=0, font=('Arial 12'), fg='white', bg='#14A769',command=ch,relief=FLAT).pack()
    Label(loginwindow,text="            ",bg=background,fg=background,font=("Copperplate Gothic Bold",6)).pack()
    lb = Label(loginwindow,text="",font=("Arial Black",9),bg="white",fg="indianred1")
    lb.pack()
    labl = Label(loginwindow,font=("ModernNo20",10), textvariable=svar, height=1,width=56)
    svar.set("")
    def shif():
        shif.msg = shif.msg[1:] + shif.msg[0]
        svar.set(shif.msg)
        loginwindow.after(deli, shif)
    shif.msg = '                     To know the secret key read this project GitHub repository.                    '
    labl.place(x=0,y=0)
    messagebox.showinfo("Thank You !!","Thank You For Use My Software")
    shif()

def exit_fun():
    a = messagebox.askquestion("Exit", "Are you sure?")
    if a == "yes":
        loginwindow.destroy()
        sys.exit()
loginwindow.wm_protocol("WM_DELETE_WINDOW",exit_fun )


def main_driver():
    loginwindow.iconbitmap(titlebar_icon)
    if not os.path.exists(userAccount_DB):
        newuser()
    else:
        login_SC()
    loginwindow.mainloop()
    return Login_suc

#main_driver()