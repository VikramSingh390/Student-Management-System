from tkinter import *
from tkinter import ttk,messagebox,filedialog
import ttkthemes
import pymysql
import time
import csv


con=None
mycursor=None



def checkConnection():
    if con==None or mycursor==None:
        messagebox.showerror('Error','Pehle database connect karo')
        return False
    return True



def clearTable():
    studentTable.delete(*studentTable.get_children())



def showStudent():
    if checkConnection()==False:
        return

    clearTable()

    try:
        query='select * from student'
        mycursor.execute(query)
        rows=mycursor.fetchall()

        for row in rows:
            studentTable.insert('',END,values=row)

    except Exception as e:
        messagebox.showerror('Error',f'Data show nahi hua\n{e}')



def exportData():
    if len(studentTable.get_children())==0:
        messagebox.showerror('Error','Table me data nahi hai')
        return

    try:
        file=filedialog.asksaveasfilename(defaultextension='.csv',
                                          filetypes=[('CSV File','*.csv'),('All Files','*.*')])

        if file=='':
            return

        with open(file,'w',newline='',encoding='utf-8') as f:
            writer=csv.writer(f)

            # heading
            writer.writerow(['Id','Name','Mobile','Email','Address','Gender','DOB','Date','Time'])

            for i in studentTable.get_children():
                row=studentTable.item(i)['values']
                writer.writerow(row)

        messagebox.showinfo('Success','Data export ho gaya')

    except Exception as e:
        messagebox.showerror('Error',f'Export nahi hua\n{e}')



def selectItem(event):
    row=studentTable.focus()
    if row:
        studentTable.selection_set(row)



def connect_database():

    def connect():
        global con,mycursor
        try:
            con=pymysql.connect(
                host=hostEntry.get().strip(),
                user=userEntry.get().strip(),
                password=passEntry.get().strip()
            )

            mycursor=con.cursor()

            query='create database if not exists studentmanagementsystem'
            mycursor.execute(query)

            query='use studentmanagementsystem'
            mycursor.execute(query)

            query='''create table if not exists student(
                    id int not null primary key,
                    name varchar(30),
                    mobile varchar(20),
                    email varchar(50),
                    address varchar(100),
                    gender varchar(10),
                    dob varchar(50),
                    date varchar(40),
                    time varchar(40)
                    )'''
            mycursor.execute(query)

            messagebox.showinfo('Success','Database connected successfully',parent=connectWindow)
            connectWindow.destroy()
            showStudent()

        except Exception as e:
            messagebox.showerror('Error',f'Connection fail\n{e}',parent=connectWindow)


    connectWindow=Toplevel()
    connectWindow.grab_set()
    connectWindow.geometry('470x250+500+230')
    connectWindow.title('Database Connection')
    connectWindow.resizable(0,0)

    Label(connectWindow,text='Host Name',font=('arial',18,'bold')).grid(row=0,column=0,padx=20,pady=15)
    hostEntry=Entry(connectWindow,font=('roman',14,'bold'),bd=2)
    hostEntry.grid(row=0,column=1,padx=20,pady=15)
    hostEntry.insert(0,'localhost')

    Label(connectWindow,text='User Name',font=('arial',18,'bold')).grid(row=1,column=0,padx=20,pady=15)
    userEntry=Entry(connectWindow,font=('roman',14,'bold'),bd=2)
    userEntry.grid(row=1,column=1,padx=20,pady=15)
    userEntry.insert(0,'root')

    Label(connectWindow,text='Password',font=('arial',18,'bold')).grid(row=2,column=0,padx=20,pady=15)
    passEntry=Entry(connectWindow,font=('roman',14,'bold'),bd=2,show='*')
    passEntry.grid(row=2,column=1,padx=20,pady=15)

    ttk.Button(connectWindow,text='Connect',command=connect).grid(row=3,column=1,pady=10)


# add student
def addStudent():
    if checkConnection()==False:
        return

    def addData():
        if idEntry.get()=='' or nameEntry.get()=='' or mobileEntry.get()=='' or emailEntry.get()=='' or addressEntry.get()=='' or genderBox.get()=='' or dobEntry.get()=='':
            messagebox.showerror('Error','Sab fields fill karo',parent=addWindow)
            return

        try:
            date=time.strftime('%d/%m/%Y')
            currenttime=time.strftime('%H:%M:%S')

            query='insert into student values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            values=(idEntry.get(),nameEntry.get(),mobileEntry.get(),emailEntry.get(),addressEntry.get(),genderBox.get(),dobEntry.get(),date,currenttime)

            mycursor.execute(query,values)
            con.commit()

            messagebox.showinfo('Success','Student add ho gaya',parent=addWindow)
            addWindow.destroy()
            showStudent()

        except pymysql.err.IntegrityError:
            messagebox.showerror('Error','Ye ID already exist karti hai',parent=addWindow)

        except Exception as e:
            messagebox.showerror('Error',f'Student add nahi hua\n{e}',parent=addWindow)


    addWindow=Toplevel()
    addWindow.grab_set()
    addWindow.geometry('500x450+450+150')
    addWindow.title('Add Student')
    addWindow.resizable(0,0)

    Label(addWindow,text='ID',font=('arial',14,'bold')).grid(row=0,column=0,padx=20,pady=10,sticky=W)
    idEntry=Entry(addWindow,font=('roman',14,'bold'),bd=2)
    idEntry.grid(row=0,column=1,padx=20,pady=10)

    Label(addWindow,text='Name',font=('arial',14,'bold')).grid(row=1,column=0,padx=20,pady=10,sticky=W)
    nameEntry=Entry(addWindow,font=('roman',14,'bold'),bd=2)
    nameEntry.grid(row=1,column=1,padx=20,pady=10)

    Label(addWindow,text='Mobile',font=('arial',14,'bold')).grid(row=2,column=0,padx=20,pady=10,sticky=W)
    mobileEntry=Entry(addWindow,font=('roman',14,'bold'),bd=2)
    mobileEntry.grid(row=2,column=1,padx=20,pady=10)

    Label(addWindow,text='Email',font=('arial',14,'bold')).grid(row=3,column=0,padx=20,pady=10,sticky=W)
    emailEntry=Entry(addWindow,font=('roman',14,'bold'),bd=2)
    emailEntry.grid(row=3,column=1,padx=20,pady=10)

    Label(addWindow,text='Address',font=('arial',14,'bold')).grid(row=4,column=0,padx=20,pady=10,sticky=W)
    addressEntry=Entry(addWindow,font=('roman',14,'bold'),bd=2)
    addressEntry.grid(row=4,column=1,padx=20,pady=10)

    Label(addWindow,text='Gender',font=('arial',14,'bold')).grid(row=5,column=0,padx=20,pady=10,sticky=W)
    genderBox=ttk.Combobox(addWindow,font=('roman',13,'bold'),state='readonly')
    genderBox['values']=('Male','Female','Other')
    genderBox.grid(row=5,column=1,padx=20,pady=10)

    Label(addWindow,text='D.O.B',font=('arial',14,'bold')).grid(row=6,column=0,padx=20,pady=10,sticky=W)
    dobEntry=Entry(addWindow,font=('roman',14,'bold'),bd=2)
    dobEntry.grid(row=6,column=1,padx=20,pady=10)
    dobEntry.insert(0,'DD/MM/YYYY')

    ttk.Button(addWindow,text='Add',command=addData).grid(row=7,columnspan=2,pady=25)


# search student
def searchStudent():
    if checkConnection()==False:
        return

    def searchData():
        clearTable()

        try:
            field=searchBox.get()
            value=searchEntry.get().strip()

            if field=='' or value=='':
                messagebox.showerror('Error','Search field aur value do',parent=searchWindow)
                return

            mapping={
                'ID':'id',
                'Name':'name',
                'Mobile':'mobile',
                'Email':'email',
                'Address':'address',
                'Gender':'gender',
                'D.O.B':'dob'
            }

            query=f"select * from student where {mapping[field]} like %s"
            mycursor.execute(query,('%'+value+'%',))
            rows=mycursor.fetchall()

            for row in rows:
                studentTable.insert('',END,values=row)

            searchWindow.destroy()

            if len(rows)==0:
                messagebox.showinfo('Result','Koi student nahi mila')

        except Exception as e:
            messagebox.showerror('Error',f'Search fail\n{e}',parent=searchWindow)


    searchWindow=Toplevel()
    searchWindow.grab_set()
    searchWindow.geometry('450x220+500+250')
    searchWindow.title('Search Student')
    searchWindow.resizable(0,0)

    Label(searchWindow,text='Search By',font=('arial',16,'bold')).grid(row=0,column=0,padx=20,pady=20)

    searchBox=ttk.Combobox(searchWindow,font=('roman',13,'bold'),state='readonly')
    searchBox['values']=('ID','Name','Mobile','Email','Address','Gender','D.O.B')
    searchBox.grid(row=0,column=1,padx=20,pady=20)

    searchEntry=Entry(searchWindow,font=('roman',14,'bold'),bd=2)
    searchEntry.grid(row=1,column=0,columnspan=2,padx=20,pady=10,ipadx=80)

    ttk.Button(searchWindow,text='Search',command=searchData).grid(row=2,columnspan=2,pady=20)


# delete student
def deleteStudent():
    if checkConnection()==False:
        return

    row=studentTable.focus()

    if row=='':
        messagebox.showerror('Error','Delete karne ke liye row select karo')
        return

    content=studentTable.item(row)
    data=content['values']
    student_id=data[0]

    ans=messagebox.askyesno('Confirm',f'ID {student_id} wala student delete karna hai?')
    if ans==False:
        return

    try:
        query='delete from student where id=%s'
        mycursor.execute(query,(student_id,))
        con.commit()

        messagebox.showinfo('Success','Student delete ho gaya')
        showStudent()

    except Exception as e:
        messagebox.showerror('Error',f'Delete nahi hua\n{e}')


# update student
def updateStudent():
    if checkConnection()==False:
        return

    row=studentTable.focus()

    if row=='':
        messagebox.showerror('Error','Update karne ke liye row select karo')
        return

    data=studentTable.item(row,'values')

    def updateData():
        if nameEntry.get()=='' or mobileEntry.get()=='' or emailEntry.get()=='' or addressEntry.get()=='' or genderBox.get()=='' or dobEntry.get()=='':
            messagebox.showerror('Error','Sab fields fill karo',parent=updateWindow)
            return

        try:
            query='''update student set
                    name=%s,
                    mobile=%s,
                    email=%s,
                    address=%s,
                    gender=%s,
                    dob=%s
                    where id=%s'''

            values=(nameEntry.get(),mobileEntry.get(),emailEntry.get(),addressEntry.get(),genderBox.get(),dobEntry.get(),data[0])

            mycursor.execute(query,values)
            con.commit()

            messagebox.showinfo('Success','Student update ho gaya',parent=updateWindow)
            updateWindow.destroy()
            showStudent()

        except Exception as e:
            messagebox.showerror('Error',f'Update nahi hua\n{e}',parent=updateWindow)


    updateWindow=Toplevel()
    updateWindow.grab_set()
    updateWindow.geometry('500x450+450+150')
    updateWindow.title('Update Student')
    updateWindow.resizable(0,0)

    Label(updateWindow,text='ID',font=('arial',14,'bold')).grid(row=0,column=0,padx=20,pady=10,sticky=W)
    idEntry=Entry(updateWindow,font=('roman',14,'bold'),bd=2)
    idEntry.grid(row=0,column=1,padx=20,pady=10)
    idEntry.insert(0,data[0])
    idEntry.config(state='readonly')

    Label(updateWindow,text='Name',font=('arial',14,'bold')).grid(row=1,column=0,padx=20,pady=10,sticky=W)
    nameEntry=Entry(updateWindow,font=('roman',14,'bold'),bd=2)
    nameEntry.grid(row=1,column=1,padx=20,pady=10)
    nameEntry.insert(0,data[1])

    Label(updateWindow,text='Mobile',font=('arial',14,'bold')).grid(row=2,column=0,padx=20,pady=10,sticky=W)
    mobileEntry=Entry(updateWindow,font=('roman',14,'bold'),bd=2)
    mobileEntry.grid(row=2,column=1,padx=20,pady=10)
    mobileEntry.insert(0,data[2])

    Label(updateWindow,text='Email',font=('arial',14,'bold')).grid(row=3,column=0,padx=20,pady=10,sticky=W)
    emailEntry=Entry(updateWindow,font=('roman',14,'bold'),bd=2)
    emailEntry.grid(row=3,column=1,padx=20,pady=10)
    emailEntry.insert(0,data[3])

    Label(updateWindow,text='Address',font=('arial',14,'bold')).grid(row=4,column=0,padx=20,pady=10,sticky=W)
    addressEntry=Entry(updateWindow,font=('roman',14,'bold'),bd=2)
    addressEntry.grid(row=4,column=1,padx=20,pady=10)
    addressEntry.insert(0,data[4])

    Label(updateWindow,text='Gender',font=('arial',14,'bold')).grid(row=5,column=0,padx=20,pady=10,sticky=W)
    genderBox=ttk.Combobox(updateWindow,font=('roman',13,'bold'),state='readonly')
    genderBox['values']=('Male','Female','Other')
    genderBox.grid(row=5,column=1,padx=20,pady=10)
    genderBox.set(data[5])

    Label(updateWindow,text='D.O.B',font=('arial',14,'bold')).grid(row=6,column=0,padx=20,pady=10,sticky=W)
    dobEntry=Entry(updateWindow,font=('roman',14,'bold'),bd=2)
    dobEntry.grid(row=6,column=1,padx=20,pady=10)
    dobEntry.insert(0,data[6])

    ttk.Button(updateWindow,text='Update',command=updateData).grid(row=7,columnspan=2,pady=25)


# title slider
count=0
text=''

def slider():
    global text,count
    if count==len(s):
        count=0
        text=''
    text=text+s[count]
    sliderLabel.config(text=text)
    count+=1
    sliderLabel.after(200,slider)



def clock():
    date=time.strftime('%d/%m/%Y')
    currenttime=time.strftime('%H:%M:%S')
    datetimeLabel.config(text=f'Date: {date}\nTime: {currenttime}')
    datetimeLabel.after(1000,clock)


# ================= GUI =================
root=ttkthemes.ThemedTk()
root.get_themes()
root.set_theme('radiance')

root.geometry('1400x900+0+0')
root.resizable(0,0)
root.title('Student Management System')


datetimeLabel=Label(root,font=('times new roman',20,'bold'),pady=10,padx=30)
datetimeLabel.place(x=5,y=5)
clock()

s='Student Management System'
sliderLabel=Label(root,text=s,font=('arial',25,'italic','bold'),width=30,padx=40)
sliderLabel.place(x=400,y=40)
slider()

connectButton=ttk.Button(root,text='Connect Database',command=connect_database)
connectButton.place(x=1150,y=10)



leftFrame=Frame(root)
leftFrame.place(x=50,y=80,width=300,height=650)

try:
    logo_Image=PhotoImage(file='students.png')
    logo_Label=Label(leftFrame,image=logo_Image)
    logo_Label.grid(row=0,column=0,pady=20)
except:
    logo_Label=Label(leftFrame,text='[ Student Image ]',font=('arial',18,'bold'))
    logo_Label.grid(row=0,column=0,pady=20)

addstudentButton=ttk.Button(leftFrame,text='Add Student',width=25,command=addStudent)
addstudentButton.grid(row=1,column=0,pady=20)

SearchstudentButton=ttk.Button(leftFrame,text='Search Student',width=25,command=searchStudent)
SearchstudentButton.grid(row=2,column=0,pady=20)

DeletestudentButton=ttk.Button(leftFrame,text='Delete Student',width=25,command=deleteStudent)
DeletestudentButton.grid(row=3,column=0,pady=20)

UpdatestudentButton=ttk.Button(leftFrame,text='Update Student',width=25,command=updateStudent)
UpdatestudentButton.grid(row=4,column=0,pady=20)

ShowstudentButton=ttk.Button(leftFrame,text='Show Student',width=25,command=showStudent)
ShowstudentButton.grid(row=5,column=0,pady=20)

ExportDataButton=ttk.Button(leftFrame,text='Export Data',width=25,command=exportData)
ExportDataButton.grid(row=6,column=0,pady=20)

ExitButton=ttk.Button(leftFrame,text='Exit',width=25,command=root.destroy)
ExitButton.grid(row=7,column=0,pady=20)



rightFrame=Frame(root)
rightFrame.place(x=350,y=80,width=1000,height=650)

scrollBarX=Scrollbar(rightFrame,orient=HORIZONTAL)
scrollBarY=Scrollbar(rightFrame,orient=VERTICAL)

studentTable=ttk.Treeview(
    rightFrame,
    columns=('Id','Name','Mobile No','Email','Address','Gender','D.O.B','Added Date','Added Time'),
    xscrollcommand=scrollBarX.set,
    yscrollcommand=scrollBarY.set
)

scrollBarX.config(command=studentTable.xview)
scrollBarY.config(command=studentTable.yview)

scrollBarX.pack(side=BOTTOM,fill=X)
scrollBarY.pack(side=RIGHT,fill=Y)

studentTable.pack(fill=BOTH,expand=1)

studentTable.heading('Id',text='Id')
studentTable.heading('Name',text='Name')
studentTable.heading('Mobile No',text='Mobile No')
studentTable.heading('Email',text='Email')
studentTable.heading('Address',text='Address')
studentTable.heading('Gender',text='Gender')
studentTable.heading('D.O.B',text='D.O.B')
studentTable.heading('Added Date',text='Added Date')
studentTable.heading('Added Time',text='Added Time')

studentTable.config(show='headings')

studentTable.column('Id',width=100,anchor=CENTER)
studentTable.column('Name',width=150,anchor=CENTER)
studentTable.column('Mobile No',width=120,anchor=CENTER)
studentTable.column('Email',width=200,anchor=CENTER)
studentTable.column('Address',width=220,anchor=CENTER)
studentTable.column('Gender',width=100,anchor=CENTER)
studentTable.column('D.O.B',width=120,anchor=CENTER)
studentTable.column('Added Date',width=120,anchor=CENTER)
studentTable.column('Added Time',width=120,anchor=CENTER)

studentTable.bind('<<TreeviewSelect>>',selectItem)

root.mainloop()