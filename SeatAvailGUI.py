from tkinter import *

textfilepath='SeatAvail/coursefile.txt'

def add_course():
    info = ''
    for e in entries:
        if len(e.get())!=0:
            info=info+e.get()+' \n'
            e.delete(0,END)
    file = open(textfilepath,'a+')
    file.write(info)
    file.close()
    view_courses()

def onDoubleClick(evt):
    # Note here that Tkinter passes an event object to onselect()
    w = evt.widget
    index = int(w.curselection()[0])
    value = w.get(index)
    w.delete(index)
    with open(textfilepath, "r") as infile:
        lines = infile.readlines()

    with open(textfilepath, "w") as outfile:
        for line in lines:
            if line!=value+'\n':
                outfile.write(line)

def clear_courses():
    open(textfilepath, 'w').close()
    view_courses()

def view_courses():
    listbox = Listbox(master,width=18,bg='light yellow',selectbackground='salmon1',highlightcolor='salmon1')
    listbox.grid(row=7)
    scrollbar = Scrollbar(listbox, orient=VERTICAL)
    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)
    with open(textfilepath,'r') as file:
        file_courses = [line.rstrip('\n') for line in file]
    for i,c in enumerate(file_courses):
        #Label(master,text=c).grid(row=7+i,sticky=W)
        listbox.insert(END,c)
    listbox.bind('<Double-Button-1>', onDoubleClick)

master = Tk()
master.title('SeatAvail')

windowWidth = master.winfo_reqwidth()
windowHeight = master.winfo_reqheight()
positionRight = int(master.winfo_screenwidth()/2 - windowWidth/2)
positionDown = int(master.winfo_screenheight()/3 - windowHeight/2)

master.geometry('380x350')
master.geometry("+{}+{}".format(positionRight, positionDown))

Label(master, text="Course Name (CSCI 183):").grid(row=0,sticky=E)
Label(master, text="Catalog Number (78501):").grid(row=2,sticky=E)
Label(master, text="Instructor (Manna):").grid(row=4,sticky=E)
Label(master, text="or").grid(row=1,column=1)
Label(master, text="or").grid(row=3,column=1)

e1 = Entry(master)
e2 = Entry(master)
e3 = Entry(master)
entries = [e1,e2,e3]

e1.grid(row=0, column=1)
e2.grid(row=2, column=1)
e3.grid(row=4, column=1)
view_courses()

Button(master, text='Clear Courses', command=clear_courses).grid(row=5, column=0, sticky=W, pady=4)
Button(master, text='Add course', command=add_course).grid(row=5, column=1, sticky=W, pady=4)

mainloop()