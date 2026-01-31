from tkinter import Tk,Label,Frame,Entry,Button,messagebox,filedialog
from tkinter.ttk import Combobox
from tkintertable import TableCanvas,TableModel
import random
import time
import projecttables
import sqlite3
import gmail
from PIL import Image,ImageTk
import os
import shutil

win=Tk()
win.state('zoomed')
win.resizable(width=False,height=False)
win.configure(bg='pink')

title=Label(win,text="Banking Automation",font=('arial',45,'bold','underline'),bg='white')
title.pack()

date=time.strftime("%d-%B-%Y")
currdate=Label(win,text=date,font=('arial',18,'bold','underline'),bg='white')
currdate.pack(pady=5)

img=Image.open("logo.jpg").resize((260,128))
bitmap_img=ImageTk.PhotoImage(img,master=win)

lbl_img=Label(win,image=bitmap_img)
lbl_img.place(relx=0,rely=0)

#Bottom part setting
footer=Label(win,text=" Presented by:Shreya Srivastava @8423364068",font=('arial',18,'bold','underline'),bg='white')
footer.pack(side="bottom")

def main_screen():
    frm=Frame(win,highlightbackground='black',highlightthickness=2)
    frm.configure(bg='powder blue')
    frm.place(relx=0,rely=.16,relwidth=1,relheight=.8)
    
    code_cap=''
    for i in range(3):
        i=random.randint(65,90)
        c=chr(i)
        j=random.randint(0,9)
        code_cap=code_cap+str(j)+c

    def forgot_pass():
        frm.destroy()
        forgotpass_screen()
    
    def login():
        acn_type=cb_type.get()
        acno=e_acn.get()
        pwd=e_pass.get()
        user_cap=e_captcha.get()

        if acno=="" or pwd=="" or user_cap=="":
             messagebox.showerror("login"," Empty fields aren't allowed!")
             return



        if acn_type=="admin" and acno=="0" and pwd=="admin" :
            if user_cap==code_cap:
               frm.destroy()
               welcome_admin_screen()
            else:
                messagebox.showerror("login","Invalid captcha  !")
   
               
        elif acn_type=="user":
            if user_cap==code_cap:
               conobj=sqlite3.connect('bank.sqlite')
               curobj=conobj.cursor()
               curobj.execute('select *from users where users_acno=? and users_pass=? ',(acno,pwd))
               tup=curobj.fetchone()
               if tup==None:
                   messagebox.showerror("Login","Invalid Acn/Pass")
                   return
               else:
                 global welcome_user,user_acno
                 welcome_user=tup[1]
                 user_acno=tup[0]
                 frm.destroy()
                 welcome_user_screen()
            else:
                messagebox.showerror("login","Invalid captcha  !")
            

        else:
            messagebox.showerror("login","Invalid acn or password !")

    lbl_type=Label(frm,text="ACN Type",font=('arial',20,'bold'),bg='pink')
    lbl_type.place(relx=.4,rely=.05)

    cb_type=Combobox(frm,values=['------select ACN type-------','user','admin'],font=('arial',20,'bold'))
    cb_type.current(0)
    cb_type.place(relx=.51,rely=0.05)

    lbl_acn=Label(frm,text="ACN No.",font=('arial',20,'bold'),bg='pink')
    lbl_acn.place(relx=.4,rely=.13)

    e_acn=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_acn.place(relx=.51,rely=0.13)
    e_acn.focus()

    lbl_pass=Label(frm,text="Password",font=('arial',20,'bold'),bg='pink')
    lbl_pass.place(relx=.4,rely=.23)

    #cap=''
    #for i in range(3):
        #i=random.randint(65,90)
        #c=chr(i)
        #j=random.randint(0,9)
        #cap=cap+str(j)+c

    def refresh():
        frm.destroy()
        main_screen()



    lbl_captcha=Label(frm,text=f"Captcha\t{code_cap}",font=('arial',25,'bold'),bg='black',fg='pink')
    lbl_captcha.place(relx=.48,rely=.33)

    btn_refresh=Button(frm,text="refresh..",font=('arial',12,),bd=5,command=refresh)
    btn_refresh.place(relx=.7,rely=.5)

    lbl_captcha2=Label(frm,text="Enter captcha",font=('arial',17,'bold'),bg='pink',fg='black')
    lbl_captcha2.place(relx=.4,rely=.43)
    


    e_captcha=Entry(frm,font=('arial',19,'bold'),bd=5,bg='black',fg='pink')
    e_captcha.place(relx=.53,rely=.43)

    e_pass=Entry(frm,font=('arial',20,'bold'),bd=4,show='*')
    e_pass.place(relx=.51,rely=.23)

    btn_login=Button(frm,text="Login..",font=('arial',16,'bold'),bd=5,command=login)
    btn_login.place(relx=.51,rely=.66)

    btn_reset=Button(frm,text="Reset..",font=('arial',16,'bold'),bd=5,command=refresh)
    btn_reset.place(relx=.67,rely=.66)
    
    btn_forgotpass=Button(frm,text="forgot password",font=('arial',16,'bold'),bd=5,command=forgot_pass)
    btn_forgotpass.place(relx=.56,rely=.77)

def forgotpass_screen():
    frm=Frame(win,highlightbackground='black',highlightthickness=2)
    frm.configure(bg='purple')
    frm.place(relx=0,rely=.16,relwidth=1,relheight=.8)
    
    def back():
        frm.destroy()
        main_screen()
    
    def reset():
        e_acn.delete(0,"end")
        e_email.delete(0,"end")
        e_mob.delete(0,"end")
        e_acn.focus()
        
        
    def forgotpass_db():
        uacno=e_acn.get()
        umob=e_mob.get()
        uemail=e_email.get()

        conobj=sqlite3.connect('bank.sqlite')
        curobj=conobj.cursor()
        curobj.execute('select users_name,users_pass from users where users_acno=? and users_email=? and users_mob=?',(uacno,uemail,umob))
        tup=curobj.fetchone()
        if tup==None:
            messagebox.showerror("Forgot Pass","Invalid Details!")
            return
        else:
            global upass,uname
            uname=tup[0]

            upass=tup[1]
            #code to generate otp
            otp=random.randint(1000,9999)
            try:
             
                con=gmail.GMail('shreyasrivastavas360@gmail.com','wltn yqdz dovo mdnh')
                utext=f''' Hello,{uname},
            OTP to recover passwprd is  {otp}
            
            Thanks
            Kenara Bank
             
            
             '''
                msg=gmail.Message(to=uemail,subject='OTP for password recovery ',text=utext)
                con.send(msg)
                messagebox.showinfo('New User',f'Mail sent successfully')
                lbl_otp=Label(frm,text="OTP",font=('arial',15,'bold'),bg='pink')
                lbl_otp.place(relx=.5,rely=.6)

                e_otp=Entry(frm,font=('arial',20,'bold'),bd=5)
                e_otp.place(relx=.59,rely=0.6)
                
                def verify_otp():
                    if otp==int(e_otp.get()):
                        messagebox.showinfo('Forgot pass',f'Your Pass is :\t{upass}')
                    else:
                        messagebox.showerror('Forgot Pass',f'Invalid OTP')

                btn_otp=Button(frm,text="verify",font=('arial',16,'bold'),bd=5,command=verify_otp)
                btn_otp.place(relx=.65,rely=.7)
            except:
                messagebox.showerror('Network problem ', 'Something went wrong with network')
            #code to sent email otp

    btn_back=Button(frm,text="<-back",font=('arial',16,'bold'),bd=5,command=back)
    btn_back.place(relx=0,rely=0)

    lbl_acn=Label(frm,text="ACN No.",font=('arial',20,'bold'),bg='pink')
    lbl_acn.place(relx=.4,rely=.13)

    e_acn=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_acn.place(relx=.51,rely=0.13)
    e_acn.focus()

    lbl_mob=Label(frm,text="Mob",font=('arial',20,'bold'),bg='pink')
    lbl_mob.place(relx=.4,rely=.23)

    e_mob=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_mob.place(relx=.51,rely=0.23)

    lbl_email=Label(frm,text="E-mail",font=('arial',20,'bold'),bg='pink')
    lbl_email.place(relx=.4,rely=.33)

    e_email=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_email.place(relx=.51,rely=0.33)

    btn_submit=Button(frm,text="Submit",font=('arial',16,'bold'),bd=5,command=forgotpass_db)
    btn_submit.place(relx=.51,rely=.48)

    btn_reset=Button(frm,text="Reset",font=('arial',16,'bold'),bd=5,command=reset)
    btn_reset.place(relx=.62,rely=.48)

def welcome_admin_screen():
    frm=Frame(win,highlightbackground='black',highlightthickness=2)
    frm.configure(bg='purple')
    frm.place(relx=0,rely=.16,relwidth=1,relheight=.8)
    
    def logout():
        frm.destroy()
        main_screen()
    
    def newuser():
        frm.destroy()
        newuser_screen()
    
    def deleteuser():
        frm.destroy()
        deleteuser_screen()

    def viewuser():
        frm.destroy()
        viewuser_screen()    


    btn_logout=Button(frm,text="Logout",font=('arial',16,'bold'),bd=5,command=logout)
    btn_logout.place(relx=0,rely=0)

    btn_newuser=Button(frm,text="Open User acn",font=('arial',20,'bold'),bd=5,bg='powder blue',command=newuser)
    btn_newuser.place(relx=.03,rely=.2,relwidth=.2)

    btn_deleteuser=Button(frm,text="Delete User Acn",command=deleteuser,font=('arial',20,'bold'),bd=5,bg='powder blue')
    btn_deleteuser.place(relx=.03,rely=.34,relwidth=.2) 

    btn_viewuser=Button(frm,text="View User Acn",command=viewuser,font=('arial',20,'bold'),bd=5,bg='powder blue')
    btn_viewuser.place(relx=.03,rely=.48,relwidth=.2) 
 
def newuser_screen():
    frm=Frame(win,highlightbackground='black',highlightthickness=2)
    frm.configure(bg='purple')
    frm.place(relx=0,rely=.16,relwidth=1,relheight=.8)
    
    def logout():
        frm.destroy()
        main_screen()
    
    def back():
        frm.destroy()
        welcome_admin_screen()

    def newuser_db():
        uname=e_name.get()
        umob=e_mob.get()
        umail=e_email.get()
        uadhar=e_adhar.get()
        ubal=0
        upass=''
        for i in range(3):
            i=random.randint(65,90)
            c=chr(i)
            j=random.randint(0,9)
            upass=upass+str(j)+c
        conobj=sqlite3.connect("bank.sqlite")
        curobj=conobj.cursor() 
        curobj.execute('insert into users(users_name,users_pass,users_mob,users_email,users_bal,users_adhar,users_opendate) values(?,?,?,?,?,?,?)',(uname,upass,umob,umail,ubal,uadhar,date))   
        conobj.commit()
        conobj.close()

        conobj=sqlite3.connect("bank.sqlite")
        curobj=conobj.cursor()
        curobj.execute('select max(users_acno) from users')
        uacn=curobj.fetchone()[0]
        conobj.close()

        messagebox.showinfo('New User',f'ACN created with ACN:{uacn} & PASS:{upass}')
        try:
             
             con=gmail.GMail('shreyasrivastavas360@gmail.com','wltn yqdz dovo mdnh')
             utext=f''' Hello,{uname},
             Your account has been opened successfully with Kenara Bank
             Your Account no  is {uacn}
             Your Password is {upass}

             Kindly change your password when you login to app
             Thanks
             Kenara Bank Corp
             '''
             msg=gmail.Message(to=umail,subject='Account opened successfully',text=utext)
             con.send(msg)
             messagebox.showinfo('New User',f'Mail sent successfully')
        except:
            messagebox.showerror('Network problem ', 'Something went wrong with network')
    #btn_logout=Button(frm,text="Logout",font=('arial',16,'bold'),bd=5,command=logout)
    #btn_logout.place(relx=.92,rely=0)

    #btn_back=Button(frm,text="<-Back",font=('arial',16,'bold'),bd=5,command=back)

        #curobj.execute('insert into users(users_name,users_pass,users_mob,users_email,users_bal,users_adhar,users_opendate) values(?,?,?,?,?,?,?)',(uname,upass,umob,umail,ubal,uadhar,date)     
    btn_logout=Button(frm,text="Logout",font=('arial',16,'bold'),bd=5,command=logout)
    btn_logout.place(relx=.92,rely=0)

    btn_back=Button(frm,text="<-Back",font=('arial',16,'bold'),bd=5,command=back)
    btn_back.place(relx=.82,rely=0)

    lbl_name=Label(frm,text="Name",font=('arial',20,'bold'),bg='pink')
    lbl_name.place(relx=.4,rely=.13)

    e_name=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_name.place(relx=.51,rely=0.13)
    e_name.focus()

    lbl_mob=Label(frm,text="Mob",font=('arial',20,'bold'),bg='pink')
    lbl_mob.place(relx=.4,rely=.23)

    e_mob=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_mob.place(relx=.51,rely=0.23)

    lbl_email=Label(frm,text="E-mail",font=('arial',20,'bold'),bg='pink')
    lbl_email.place(relx=.4,rely=.33)

    e_email=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_email.place(relx=.51,rely=0.33)

    lbl_adhar=Label(frm,text="Adhar",font=('arial',20,'bold'),bg='pink')
    lbl_adhar.place(relx=.4,rely=.43)

    e_adhar=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_adhar.place(relx=.51,rely=0.43)

    btn_submit=Button(frm,text="Submit",font=('arial',16,'bold'),bd=5,command=newuser_db)
    btn_submit.place(relx=.51,rely=.6)

    btn_reset=Button(frm,text="Reset",font=('arial',16,'bold'),bd=5,command=back)
    btn_reset.place(relx=.62,rely=.6)

def deleteuser_screen():
    frm=Frame(win,highlightbackground='black',highlightthickness=2)
    frm.configure(bg='purple')
    frm.place(relx=0,rely=.16,relwidth=1,relheight=.8)
    
    def logout():
        frm.destroy()
        main_screen()
    
    def back():
        frm.destroy()
        welcome_admin_screen()

    def delete():
        uacn=e_acn.get()
        uadhar=e_adhar.get()
        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        curobj.execute('delete from users where users_acno=? and users_adhar=? ',(uacn,uadhar))
        curobj.execute('delete from txn where txn_acno=? ',(uacn,))
        conobj.commit()
        conobj.close()
        messagebox.showinfo("Delete Users","Account deleted")

    btn_logout=Button(frm,text="Logout",font=('arial',16,'bold'),bd=5,command=logout)
    btn_logout.place(relx=.92,rely=0)

    btn_back=Button(frm,text="<-Back",font=('arial',16,'bold'),bd=5,command=back)
    btn_back.place(relx=0,rely=0)

    lbl_acn=Label(frm,text="Acn No.",font=('arial',20,'bold'),bg='pink')
    lbl_acn.place(relx=.4,rely=.33)

    e_acn=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_acn.place(relx=.51,rely=0.33)

    lbl_adhar=Label(frm,text="Adhar",font=('arial',20,'bold'),bg='pink')
    lbl_adhar.place(relx=.4,rely=.43)

    e_adhar=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_adhar.place(relx=.51,rely=0.43)

    btn_submit=Button(frm,text="Submit",font=('arial',16,'bold'),bd=5,command=delete)
    btn_submit.place(relx=.51,rely=.6)

    btn_reset=Button(frm,text="Reset",font=('arial',16,'bold'),bd=5,command=back)
    btn_reset.place(relx=.62,rely=.6)   

def viewuser_screen():
    frm=Frame(win,highlightbackground='black',highlightthickness=2)
    frm.configure(bg='purple')
    frm.place(relx=0,rely=.16,relwidth=1,relheight=.8)
    
    def logout():
        frm.destroy()
        main_screen()
    
    def back():
        frm.destroy()
        welcome_admin_screen()

    def view():
        uacn=e_acn.get()
        conobj=sqlite3.connect("bank.sqlite")
        curobj=conobj.cursor() 
        curobj.execute("select * from users where users_acno=?",(uacn,))
        tup=curobj.fetchone()
        conobj.close()
        if tup==None:
            messagebox.showerror("View","Account does not exists")
            return
        lbl_acn=Label(frm,text="Acnno.",font=('arial',23,'bold','underline'),bg='powder blue',fg='purple')
        lbl_acn.place(relx=0.25,rely=0.25)

        lbl_acn_value=Label(frm,text=tup[0],font=('arial',25,'bold','underline'),bg='white',fg='purple')
        lbl_acn_value.place(relx=0.4,rely=0.25)

        lbl_name=Label(frm,text="Name",font=('arial',23,'bold','underline'),bg='powder blue',fg='purple')
        lbl_name.place(relx=0.25,rely=0.35)

        lbl_name_value=Label(frm,text=tup[1],font=('arial',25,'bold','underline'),bg='white',fg='purple')
        lbl_name_value.place(relx=0.4,rely=0.35)

        lbl_mob=Label(frm,text="Mobno",font=('arial',23,'bold','underline'),bg='powder blue',fg='purple')
        lbl_mob.place(relx=0.25,rely=0.45)

        lbl_mob_value=Label(frm,text=tup[3],font=('arial',25,'bold','underline'),bg='white',fg='purple')
        lbl_mob_value.place(relx=0.4,rely=0.45)

        lbl_adhar=Label(frm,text="Adharno",font=('arial',23,'bold','underline'),bg='powder blue',fg='purple')
        lbl_adhar.place(relx=0.25,rely=0.55)

        lbl_adhar_value=Label(frm,text=tup[6],font=('arial',25,'bold','underline'),bg='white',fg='purple')
        lbl_adhar_value.place(relx=0.4,rely=0.55)

        lbl_opendate=Label(frm,text="Open date",font=('arial',23,'bold','underline'),bg='powder blue',fg='purple')
        lbl_opendate.place(relx=0.25,rely=0.65)

        lbl_opendate_value=Label(frm,text=tup[7],font=('arial',25,'bold','underline'),bg='white',fg='purple')
        lbl_opendate_value.place(relx=0.4,rely=0.65)

        lbl_bal=Label(frm,text="Balance",font=('arial',23,'bold','underline'),bg='powder blue',fg='purple')
        lbl_bal.place(relx=0.25,rely=0.75)

        lbl_bal_value=Label(frm,text=tup[5],font=('arial',25,'bold','underline'),bg='white',fg='purple')
        lbl_bal_value.place(relx=0.4,rely=0.75)



    btn_logout=Button(frm,text="Logout",font=('arial',16,'bold'),bd=5,command=logout)
    btn_logout.place(relx=.92,rely=0)

    btn_back=Button(frm,text="<-Back",font=('arial',16,'bold'),bd=5,command=back)
    btn_back.place(relx=0,rely=0)

    lbl_acn=Label(frm,text="Acn No.",font=('arial',20,'bold'),bg='pink')
    lbl_acn.place(relx=.25,rely=.15)

    e_acn=Entry(frm,font=('arial',20,'bold'),bd=5)
    e_acn.place(relx=.4,rely=0.15)

    btn_search=Button(frm,text="Search-->",font=('arial',16,'bold'),bd=5,command=view)
    btn_search.place(relx=.65,rely=.15)
    
def welcome_user_screen():
    frm=Frame(win,highlightbackground='black',highlightthickness=2)
    frm.configure(bg='purple')
    frm.place(relx=0,rely=.16,relwidth=1,relheight=.8)

    screen_title="User Home Screen"
    frm_title=Label(frm,text=screen_title,font=('arial',20,'bold','underline'),bg='powder blue',fg='purple')
    frm_title.pack()

    frm_wel=Label(frm,text=f"Welcome,{welcome_user}",font=('arial',20,'bold','underline'),bg='powder blue',fg='purple')
    frm_wel.place(relx=0,rely=0)

    def logout():
        frm.destroy()
        main_screen()
    
    def deposit_screen():
        screen_title=" User Deposit Screen"
        frm_title.configure(text=screen_title)

        def deposit():
            uamt=int(e_amt.get())
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            curobj.execute('update users set users_bal=users_bal+? where users_acno=?',(uamt,user_acno))
            conobj.commit()
            conobj.close()

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            curobj.execute('select users_bal from users where users_acno=?',(user_acno,))
            ubal=curobj.fetchone()[0]
            conobj.close()

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            curobj.execute('insert into txn(txn_acno,txn_type,txn_amt,txn_bal,txn_date) values(?,?,?,?,?)',(user_acno,'Cr',uamt,ubal,date))
            conobj.commit()
            conobj.close()

            messagebox.showinfo("Deposit",f"{uamt} deposited,Updated Bal:{ubal}")

        
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.3,rely=.19,relwidth=.67,relheight=.79)
        
        lbl_amt=Label(ifrm,text="Amount",font=('arial',23,'bold'),bg='pink')
        lbl_amt.place(relx=.12,rely=.17)

        e_amt=Entry(ifrm,font=('arial',23,'bold'),bd=5)
        e_amt.place(relx=.3,rely=0.17)

        btn_submit=Button(ifrm,text="Submit-->",font=('arial',16,'bold'),bd=5,command=deposit)
        btn_submit.place(relx=.72,rely=.34)




    def withdraw_screen():
        screen_title=" User withdraw Screen"
        frm_title.configure(text=screen_title)
        
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.3,rely=.19,relwidth=.67,relheight=.79)
        
        def withdraw():
            uamt=int(e_amt.get())

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            curobj.execute('select users_bal from users where users_acno=?',(user_acno,))
            ubal=curobj.fetchone()[0]
            conobj.close()
            
            
            if ubal>uamt:

            

                conobj=sqlite3.connect(database='bank.sqlite')
                curobj=conobj.cursor()
                curobj.execute('update users set users_bal=users_bal-? where users_acno=?',(uamt,user_acno))
                conobj.commit()
                conobj.close()



            

                conobj=sqlite3.connect(database='bank.sqlite')
                curobj=conobj.cursor()
                curobj.execute('insert into txn(txn_acno,txn_type,txn_amt,txn_bal,txn_date) values(?,?,?,?,?)',(user_acno,'Dr',uamt,ubal-uamt,date))
                conobj.commit()
                conobj.close()

                messagebox.showinfo("Withdraw",f"{uamt} withdrawn ,Updated Bal:{ubal-uamt}")
            else:
                messagebox.showerror("Withdraw",f"Insufficient Bal:{ubal}")    



        lbl_amt=Label(ifrm,text="Amount",font=('arial',23,'bold'),bg='pink')
        lbl_amt.place(relx=.12,rely=.17)

        e_amt=Entry(ifrm,font=('arial',23,'bold'),bd=5)
        e_amt.place(relx=.3,rely=0.17)

        btn_submit=Button(ifrm,text="Submit-->",font=('arial',16,'bold'),bd=5,command=withdraw)
        btn_submit.place(relx=.72,rely=.34)


    def transfer_screen():
        screen_title=" User Transfer Screen"
        frm_title.configure(text=screen_title)
        
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.3,rely=.19,relwidth=.67,relheight=.79)
        
        def transfer():
            uamt=int(e_amt.get())
            utoacn=int(e_to.get())

            conobj=sqlite3.connect('bank.sqlite')
            curobj=conobj.cursor()
            curobj.execute('select *from users where users_acno=?',(utoacn,))
            tup=curobj.fetchone()
            conobj.close()
            if tup==None:
                messagebox.showerror("Transfer","Invalid To Acn")
                
            #else:
                conobj=sqlite3.connect(databse='bank.sqlite')
                curobj=conobj.cursor()
                curobj.execute('select users_bal from users where users_acno=?',(user_acno,))
                ubal=curobj.fetchone()[0]
                conobj.close()
            
            
                if ubal>uamt:


            

                    conobj=sqlite3.connect(database='bank.sqlite')
                    curobj=conobj.cursor()
                    curobj.execute('update users set users_bal=users_bal-? where users_acno=?',(uamt,user_acno))
                    curobj.execute('update users set users_bal=users_bal+? where users_acno=?',(uamt,utoacn))
                    conobj.commit()
                    conobj.close()



            

                    conobj=sqlite3.connect(database='bank.sqlite')
                    curobj=conobj.cursor()
                    curobj.execute('insert into txn(txn_acno,txn_type,txn_amt,txn_bal,txn_date) values(?,?,?,?,?)',(user_acno,'Dr',uamt,ubal-uamt,date))
                    curobj.execute('insert into txn(txn_acno,txn_type,txn_amt,txn_bal,txn_date) values(?,?,?,?,?)',(utoacn,'Cr',uamt,ubal+uamt,date))
                    conobj.commit()
                    conobj.close()

                    messagebox.showinfo("Transfer",f"{uamt} transfered ,Updated Bal:{ubal-uamt}")
                else:
                    messagebox.showerror("Transfer",f"Insufficient Bal:{ubal}")
        lbl_to=Label(ifrm,text="To Acn",font=('arial',23,'bold'),bg='pink')
        lbl_to.place(relx=.12,rely=.33)

        e_to=Entry(ifrm,font=('arial',23,'bold'),bd=5)
        e_to.place(relx=.3,rely=0.33)

        lbl_amt=Label(ifrm,text="Amount",font=('arial',23,'bold'),bg='pink')
        lbl_amt.place(relx=.12,rely=.5)

        e_amt=Entry(ifrm,font=('arial',23,'bold'),bd=5)
        e_amt.place(relx=.3,rely=0.5)


        btn_submit=Button(ifrm,text="Submit-->",font=('arial',16,'bold'),bd=5,command=transfer)
        btn_submit.place(relx=.43,rely=.67)    




    def update_screen():
        screen_title=" User Update Screen"
        frm_title.configure(text=screen_title)
        
        def update_db():
            upass=e_pass.get()
            umob=e_mob.get()
            uemail=e_email.get()
            conobj=sqlite3.connect("bank.sqlite")
            curobj=conobj.cursor()
            curobj.execute('update users set users_pass=?,users_mob=?,users_email=? where users_acno=?',(upass,umob,uemail,user_acno))
            conobj.commit()
            conobj.close()
            messagebox.showinfo("Update Details","Updated")

        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.3,rely=.19,relwidth=.67,relheight=.79)
        
        lbl_pass=Label(ifrm,text="Password",font=('arial',23,'bold'),bg='pink')
        lbl_pass.place(relx=.12,rely=.17)

        e_pass=Entry(ifrm,font=('arial',23,'bold'),bd=5)
        e_pass.place(relx=.3,rely=0.17)

        lbl_mob=Label(ifrm,text="Mobileno.",font=('arial',23,'bold'),bg='pink')
        lbl_mob.place(relx=.12,rely=.33)

        e_mob=Entry(ifrm,font=('arial',23,'bold'),bd=5)
        e_mob.place(relx=.3,rely=0.33)

        lbl_email=Label(ifrm,text="E-Mail",font=('arial',23,'bold'),bg='pink')
        lbl_email.place(relx=.12,rely=.5)

        e_email=Entry(ifrm,font=('arial',23,'bold'),bd=5)
        e_email.place(relx=.3,rely=0.5)


        btn_submit=Button(ifrm,text="Submit-->",font=('arial',16,'bold'),bd=5,command=update_db)
        btn_submit.place(relx=.43,rely=.67)

        #def get_detail_db():
        conobj=sqlite3.connect("bank.sqlite")
        curobj=conobj.cursor() 
        curobj.execute("select users_pass,users_mob,users_email from users where users_acno=?",(user_acno,))
        tup=curobj.fetchone()
        conobj.close()

        e_pass.insert(0,tup[0])
        e_mob.insert(0,tup[1])
        e_email.insert(0,tup[2])

    def history_screen():
        screen_title=" User Txn History Screen"
        frm_title.configure(text=screen_title)
        
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.3,rely=.19,relwidth=.67,relheight=.79)

        data={}
        conobj=sqlite3.connect("bank.sqlite")
        curobj=conobj.cursor() 
        curobj.execute("select * from txn where txn_acno=?",(user_acno,))
        tups=curobj.fetchall()
        i=1
        for tup in tups:
            data[str(i)]={'Txn Amt':tup[3],'Txn Type':tup[2],'Updated Bal':tup[4],'Txn Date':tup[5],'Txn Id':tup[0]}
            i+=1
        model = TableModel()
        model.importDict(data)

        table_frm=Frame(ifrm)
        table_frm.place(relx=.2,rely=.2)
        table = TableCanvas(table_frm, model=model,editable=False)
        table.show()


    def details_screen():
        screen_title=" User Details Screen"
        frm_title.configure(text=screen_title)
        
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.3,rely=.19,relwidth=.67,relheight=.79)
        
        conobj=sqlite3.connect("bank.sqlite")
        curobj=conobj.cursor() 
        curobj.execute("select * from users where users_acno=?",(user_acno,))
        tup=curobj.fetchone()
        conobj.close()

        lbl_acn=Label(ifrm,text="Acnno.",font=('arial',23,'bold','underline'),bg='powder blue',fg='purple')
        lbl_acn.place(relx=0.09,rely=0.1)

        lbl_acn_value=Label(ifrm,text=tup[0],font=('arial',25,'bold','underline'),bg='white',fg='purple')
        lbl_acn_value.place(relx=0.4,rely=0.1)

        lbl_name=Label(ifrm,text="Name",font=('arial',23,'bold','underline'),bg='powder blue',fg='purple')
        lbl_name.place(relx=0.09,rely=0.25)

        lbl_name_value=Label(ifrm,text=tup[1],font=('arial',25,'bold','underline'),bg='white',fg='purple')
        lbl_name_value.place(relx=0.4,rely=0.25)

        lbl_mob=Label(ifrm,text="Mobno",font=('arial',23,'bold','underline'),bg='powder blue',fg='purple')
        lbl_mob.place(relx=0.09,rely=0.4)

        lbl_mob_value=Label(ifrm,text=tup[3],font=('arial',25,'bold','underline'),bg='white',fg='purple')
        lbl_mob_value.place(relx=0.4,rely=0.4)

        lbl_adhar=Label(ifrm,text="Adharno",font=('arial',23,'bold','underline'),bg='powder blue',fg='purple')
        lbl_adhar.place(relx=0.09,rely=0.55)

        lbl_adhar_value=Label(ifrm,text=tup[6],font=('arial',25,'bold','underline'),bg='white',fg='purple')
        lbl_adhar_value.place(relx=0.4,rely=0.55)

        lbl_opendate=Label(ifrm,text="Open date",font=('arial',23,'bold','underline'),bg='powder blue',fg='purple')
        lbl_opendate.place(relx=0.09,rely=0.7)

        lbl_opendate_value=Label(ifrm,text=tup[7],font=('arial',25,'bold','underline'),bg='white',fg='purple')
        lbl_opendate_value.place(relx=0.4,rely=0.7)

        lbl_bal=Label(ifrm,text="Balance",font=('arial',23,'bold','underline'),bg='powder blue',fg='purple')
        lbl_bal.place(relx=0.09,rely=0.85)

        lbl_bal_value=Label(ifrm,text=tup[5],font=('arial',25,'bold','underline'),bg='white',fg='purple')
        lbl_bal_value.place(relx=0.4,rely=0.85)

    def update_picture():
        img_path=filedialog.askopenfilename()
        shutil.copy(img_path,f'{user_acno}.png')
        

        pro_img=Image.open(f'{user_acno}.png').resize((240,90))
        pro_bitmap_img=ImageTk.PhotoImage(pro_img,master=frm)

        prolbl_img=Label(frm,image=pro_bitmap_img)
        prolbl_img.image=pro_bitmap_img

        prolbl_img.place(relx=0.05,rely=.07)

    btn_logout=Button(frm,text="Logout",font=('arial',16,'bold'),bd=5,command=logout)
    btn_logout.place(relx=.92,rely=0)

    if os.path.exists(f'{user_acno}.png'):
        pro_img=Image.open(f'{user_acno}.png').resize((240,90))

    else:
        pro_img=Image.open('userpro.jpg').resize((240,90))
    pro_bitmap_img=ImageTk.PhotoImage(pro_img,master=frm)

    prolbl_img=Label(frm,image=pro_bitmap_img)
    prolbl_img.image=pro_bitmap_img
    prolbl_img.place(relx=0.05,rely=.07)

    btn_update_pro=Button(frm,text="update..",font=('arial',7,'bold'),bd=2,command=update_picture)
    btn_update_pro.place(relx=.22,rely=0.21) 

    btn_details=Button(frm,text="Check Details",command=details_screen,font=('arial',20,'bold'),bd=5,bg='powder blue')
    btn_details.place(relx=.03,rely=.24,relwidth=.2)

    btn_deposit=Button(frm,text="Deposit",command=deposit_screen,font=('arial',20,'bold'),bd=5,bg='powder blue')
    btn_deposit.place(relx=.03,rely=.36,relwidth=.2) 
    
    btn_withdraw=Button(frm,text="Withdraw",command=withdraw_screen,font=('arial',20,'bold'),bd=5,bg='powder blue')
    btn_withdraw.place(relx=.03,rely=.48,relwidth=.2) 
    
    btn_update=Button(frm,text="Update",command=update_screen,font=('arial',20,'bold'),bd=5,bg='powder blue')
    btn_update.place(relx=.03,rely=.6,relwidth=.2)

    btn_transfer=Button(frm,text="Transfer",command=transfer_screen,font=('arial',20,'bold'),bd=5,bg='powder blue')
    btn_transfer.place(relx=.03,rely=.73,relwidth=.2)

    btn_history=Button(frm,text=" TXN History",command=history_screen,font=('arial',20,'bold'),bd=5,bg='powder blue')
    btn_history.place(relx=.03,rely=.87,relwidth=.2) 


    #btn_viewuser=Button(frm,text="View User Acn",command=viewuser,font=('arial',20,'bold'),bd=5,bg='powder blue')
    #btn_viewuser.place(relx=.03,rely=.7,relwidth=.2)    

main_screen()





win.mainloop()
