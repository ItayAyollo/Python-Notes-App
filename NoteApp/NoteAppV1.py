import tkinter
from tkinter import *
import tkinter.messagebox
from tkinter import filedialog  # TODO: colors mean stuff (red = urgent, blue = reminder, yellow = todo list) !DONE!
import random
from PIL import Image
from win10toast import ToastNotifier
from threading import Thread
import time

root = Tk()
toaster = ToastNotifier()

root.title("Note Taker")
version = "V1.0.2"
var = StringVar()
var.set(version)

bg = PhotoImage(file="Background.png")
im = Image.open("Background.png")
rbg = PhotoImage(file="BackgroundReminder.png")
rim = Image.open("BackgroundReminder.png")
ubg = PhotoImage(file="BackgroundUrgent.png")
uim = Image.open("BackgroundUrgent.png")
tbg = PhotoImage(file="BackgroundTodo.png")
tim = Image.open("BackgroundTodo.png")
icon_location = 'Icon.ico'
root.iconbitmap(icon_location)

focus_value = 0.8
countdown_time=120

location = 'Colors.txt'  # location of the colors file

# #FF6F69 a nice shade of red
# #7289DA pretty cool shade of blue
# #FFEEAD skin tone yellow
# #52BF90 nice green

def lost_focus(*args):
    """triggers when the window loses focus."""
    if j.get() == 0:
        root.attributes("-alpha", focus_value)
        print("lost focus")


def gained_focus(*args):
    """triggers when the window loses focus."""
    root.attributes("-alpha", 1)
    print("gained focus")


root.bind('<FocusIn>', gained_focus)
root.bind('<FocusOut>', lost_focus)


def stay_on_top():  # controls the "stay on top" stuff
    print(i.get())
    if i.get() == 1:
        root.attributes('-topmost', True)  # sets the window to be the topmost windows
        root.update()
    else:
        root.attributes('-topmost', False)  # same thing but false
        root.update()


#lines = open(location).read().splitlines()
#myline = random.choice(lines)
#print(myline)  # all of this is to pick a random color from Colors.txt and set it as the background color of the window

#root['background'] = myline

label1 = Label(root, image=bg)
label1.place(x=0, y=0)

root['background'] = '#52BF90'
root.update()
label1.config(bg='#52BF90')
label1.update()

#root.wm_attributes('-transparentcolor', '#f700ff')


def file1():  # new note
    if not textBox.edit_modified():
        textBox.delete('1.0', tkinter.END)
    else:
        savefileas()
        textBox.delete('1.0', tkinter.END)

    textBox.edit_modified(0)
#    lines = open(location).read().splitlines()
#    myline = random.choice(lines)
#    print(myline)


def openfile():  # open an existing note
    if not textBox.edit_modified():
        try:
            path = filedialog.askopenfile(filetypes=(("Text files", "*.txt"), ("All files", "*.*"))).name

            root.title('Note - ' + path)

            with open(path, 'r') as f:
                content = f.read()
                textBox.delete('1.0', tkinter.END)
                textBox.insert('1.0', content)

                textBox.edit_modified(0)

        except:
            savefileas()

            textBox.edit_modified(0)
            openfile()


def savefilebeforeclose():  # save current note before closing
    try:

        path = root.title().split('-')[1][1:]

    except:
        path = ''

    if path != '':

        with open(path, 'w') as f:
            content = textBox.get('1.0', tkinter.END)
            f.write(content)

    else:
        savefileas()

    textBox.edit_modified(0)
    root.destroy()


def savefile():  # save note
    try:

        path = root.title().split('-')[1][1:]

    except:
        path = ''

    if path != '':

        with open(path, 'w') as f:
            content = textBox.get('1.0', tkinter.END)
            f.write(content)

    else:
        savefileas()

    textBox.edit_modified(0)


def savefileas():  # save note as
    try:
        path = filedialog.asksaveasfile(filetypes=(("Text files", "*.txt"), ("All files", "*.*"))).name
        root.title('Note - ' + path)

    except:
        return

    with open(path, 'w') as f:
        f.write(textBox.get('1.0', tkinter.END))


def on_closing():  # when user tries to close the program(either by pressing X, alt f4 or any other method) this gets called
    if not textBox.edit_modified():
        root.destroy()
    else:
        if tkinter.messagebox.askyesno("Save note?", "Wanna save your note before closing?"):
            savefilebeforeclose()
        else:
            root.destroy()


def reminder():
    toasttext = textBox.get('1.0', tkinter.END)
    if not textBox.edit_modified():
        toaster.show_toast("Dont Forget Your task!", "This is the task reminder you've set", icon_path=icon_location,
                           duration=15, threaded=True)
    else:
        toaster.show_toast("Dont forget Your task: " + toasttext, "This is the task reminder you've set",
                           icon_path=icon_location,
                           duration=15, threaded=True)


def timer(arg):
    time.sleep(arg)
    reminder()


def five_min():  # this is 'poop', switch to [root.after] if you have time because using threads is scary
    thread = Thread(target=timer, args=(300,))
    thread.start()


def ten_min():  # this is 'poop', switch to [root.after] if you have time because using threads is scary
    thread = Thread(target=timer, args=(600,))
    thread.start()


def fifteen_min():  # this is 'poop', switch to [root.after] if you have time because using threads is scary
    thread = Thread(target=timer, args=(900,))
    thread.start()


j = IntVar()  # save the state of "dont make transparent" check box

i = IntVar()  # saves the state of the "stay on top" checkbox (1 = true, 0 = false)
c = Checkbutton(root, text="Stay On Top", variable=i, command=stay_on_top)  # stay on top checkbox
c.pack()
c.place(relx=0.5, rely=0.1, anchor=CENTER)

b = Button(root, text="New Note", command=file1)  # new note button
b.pack()
b.place(relx=0.5, rely=0.85, anchor=CENTER)

remindercanvas = Canvas(root, width=240, relief=FLAT, height=300, bg='#7289DA')  # Reminder Stuff
rmd1 = Button(root, text='remind me in 5 min', command=five_min)
rmd2 = Button(root, text='remind me in 10 min', command=ten_min)
rmd3 = Button(root, text='remind me in 15 min', command=fifteen_min)

urgentcanvas = Canvas(root, width=240, relief=FLAT, height=300, bg='#FF6F69')  # Urgent Stuff
labelj = tkinter.Label(root)

def countdown(count):  # Urgent Stuff
    e = k.get()
    # change text in label
    labelj['text'] = count

    if e == 2:
        if count > 0:
            #print("im still counting, after all this time!")
            root.after(1000, countdown, count-1)  # call countdown again after 1000ms (1s)
        if count <= 0:
            reminder()
            countdown(countdown_time)

### The text area ###
textBox = tkinter.Text(root, relief=GROOVE, height=10, width=25, font=("Helvetica", 16))
textBox.pack()
textBox.place(relx=0.5, rely=0.5, anchor=CENTER)
### end of text area ###

def todo_controller():
    if ch1.get() == 1:
        textBox1.config(state='disabled', bg='#E5E5E5')
        root.update()
    else:
        textBox1.config(state='normal', bg='#FFFFFF')
        root.update()

    if ch2.get() == 1:
        textBox2.config(state='disabled', bg='#E5E5E5')
        root.update()
    else:
        textBox2.config(state='normal', bg='#FFFFFF')
        root.update()

    if ch3.get() == 1:
        textBox3.config(state='disabled', bg='#E5E5E5')
        root.update()
    else:
        textBox3.config(state='normal', bg='#FFFFFF')
        root.update()

    if ch4.get() == 1:
        textBox4.config(state='disabled', bg='#E5E5E5')
        root.update()
    else:
        textBox4.config(state='normal', bg='#FFFFFF')
        root.update()

    if ch5.get() == 1:
        textBox5.config(state='disabled', bg='#E5E5E5')
        root.update()
    else:
        textBox5.config(state='normal', bg='#FFFFFF')
        root.update()

    if ch1.get() == 1 and ch2.get() == 1 and ch3.get() == 1 and ch4.get() == 1 and ch5.get() == 1:  # my brain hurts
        if tkinter.messagebox.askyesno("Clear List?", "Would you like to clear your list?"):
            ch1.set(0)
            ch2.set(0)
            ch3.set(0)
            ch4.set(0)
            ch5.set(0)
            todo_controller()
            textBox1.delete('1.0', tkinter.END)
            textBox2.delete('1.0', tkinter.END)
            textBox3.delete('1.0', tkinter.END)
            textBox4.delete('1.0', tkinter.END)
            textBox5.delete('1.0', tkinter.END)
        else:
            print("user decided not to clear todo list")

def todo_reset():  # this gets done when user clicks the reset to-do list button.
    ch1.set(0)
    ch2.set(0)
    ch3.set(0)
    ch4.set(0)
    ch5.set(0)
    todo_controller()
    textBox1.delete('1.0', tkinter.END)
    textBox2.delete('1.0', tkinter.END)
    textBox3.delete('1.0', tkinter.END)
    textBox4.delete('1.0', tkinter.END)
    textBox5.delete('1.0', tkinter.END)

todocanvas = Canvas(root, width=300, relief=FLAT, height=240, bg='#FFEEAD')
textBox1 = tkinter.Text(root, height=2, width=25, wrap='none', font=("Helvetica", 12), relief=RAISED )
ch1=IntVar()
check1 = Checkbutton(root, text = "DONE", variable=ch1, command=todo_controller)

textBox2 = tkinter.Text(root, height=2, width=25, wrap='none', font=("Helvetica", 12), relief=RAISED )
ch2=IntVar()
check2 = Checkbutton(root, text = "DONE", variable=ch2, command=todo_controller)

textBox3 = tkinter.Text(root, height=2, width=25, wrap='none', font=("Helvetica", 12), relief=RAISED)
ch3=IntVar()
check3 = Checkbutton(root, text = "DONE", variable=ch3, command=todo_controller)

textBox4 = tkinter.Text(root, height=2, width=25, wrap='none', font=("Helvetica", 12), relief=RAISED )
ch4=IntVar()
check4 = Checkbutton(root, text = "DONE", variable=ch4, command=todo_controller)

textBox5 = tkinter.Text(root, height=2, width=25, wrap='none', font=("Helvetica", 12), relief=RAISED )
ch5=IntVar()
check5 = Checkbutton(root, text = "DONE", variable=ch5, command=todo_controller)

todoreset = Button(root, text='Reset Todo List', command=todo_reset)


def reseter():
    remindercanvas.place(relx=0.5, rely=800, anchor=CENTER)
    rmd1.place(relx=0.5, rely=800, anchor=CENTER)
    rmd2.place(relx=0.5, rely=800, anchor=CENTER)
    rmd3.place(relx=0.5, rely=800, anchor=CENTER)
    urgentcanvas.place(relx=0.5, rely=800, anchor=CENTER)
    labelj.place(relx=0.5, rely=800, anchor=CENTER)
    urgentcanvas.pack_forget()
    labelj.pack_forget()
    remindercanvas.pack_forget()
    rmd1.pack_forget()
    rmd2.pack_forget()
    rmd3.pack_forget()

    b.place(relx=0.5, rely=0.85, anchor=CENTER)
    root['background'] = '#52BF90'
    root.update()
    label1.config(bg='#52BF90')
    label1.config(image=bg)
    label1.update()

    todocanvas.pack_forget()
    todocanvas.place(relx=0.5, rely=800, anchor=CENTER)
    textBox1.pack_forget()
    textBox1.place(relx=0.4, rely=800.3, anchor=CENTER)
    check1.pack_forget()
    check1.place(relx=0.89, rely=800.3, anchor=CENTER)
    textBox2.pack_forget()
    textBox2.place(relx=0.4, rely=800.4, anchor=CENTER)
    check2.pack_forget()
    check2.place(relx=0.89, rely=800.4, anchor=CENTER)
    textBox3.pack_forget()
    textBox3.place(relx=0.4, rely=800.5, anchor=CENTER)
    check3.pack_forget()
    check3.place(relx=0.89, rely=8005, anchor=CENTER)
    textBox4.pack_forget()
    textBox4.place(relx=0.4, rely=800.6, anchor=CENTER)
    check4.pack_forget()
    check4.place(relx=0.89, rely=800.6, anchor=CENTER)
    textBox5.pack_forget()
    textBox5.place(relx=0.4, rely=800.7, anchor=CENTER)
    check5.pack_forget()
    check5.place(relx=0.89, rely=800.7, anchor=CENTER)
    todoreset.pack_forget()
    todoreset.place(relx=0.5, rely=800.91, anchor=CENTER)

def modes():
    e = k.get()

    if e == 4:  # TO-DO LIST MODE
        reseter()
        file1()
        root['background'] = '#FFEEAD'
        root.update()
        label1.config(bg='#FFEEAD')
        label1.config(image=tbg)
        label1.update()
        todocanvas.pack()
        todocanvas.place(relx=0.5, rely=0.5, anchor=CENTER)
        textBox1.pack()
        textBox1.place(relx=0.4, rely=0.3, anchor=CENTER)
        check1.pack()
        check1.place(relx=0.89, rely=0.3, anchor=CENTER)
        textBox2.pack()
        textBox2.place(relx=0.4, rely=0.4, anchor=CENTER)
        check2.pack()
        check2.place(relx=0.89, rely=0.4, anchor=CENTER)
        textBox3.pack()
        textBox3.place(relx=0.4, rely=0.5, anchor=CENTER)
        check3.pack()
        check3.place(relx=0.89, rely=0.5, anchor=CENTER)
        textBox4.pack()
        textBox4.place(relx=0.4, rely=0.6, anchor=CENTER)
        check4.pack()
        check4.place(relx=0.89, rely=0.6, anchor=CENTER)
        textBox5.pack()
        textBox5.place(relx=0.4, rely=0.7, anchor=CENTER)
        check5.pack()
        check5.place(relx=0.89, rely=0.7, anchor=CENTER)
        todoreset.pack()
        todoreset.place(relx=0.5, rely=0.85, anchor=CENTER)
        b.place(relx=0.5, rely=800.85, anchor=CENTER)

    if e == 3:  # REMINDER MODE
        reseter()
        remindercanvas.pack()
        remindercanvas.place(relx=0.5, rely=1, anchor=CENTER)
        rmd1.pack()
        rmd1.place(relx=0.5, rely=0.85, anchor=CENTER)
        rmd2.pack()
        rmd2.place(relx=0.5, rely=0.91, anchor=CENTER)
        rmd3.pack()
        rmd3.place(relx=0.5, rely=0.97, anchor=CENTER)
        root['background'] = '#7289DA'
        root.update()
        label1.config(bg='#7289DA')
        label1.config(image=rbg)
        label1.update()

    if e == 2:  # URGENT MODE
        reseter()
        root['background'] = '#FF6F69'
        root.update()
        label1.config(bg='#FF6F69')
        label1.config(image=ubg)
        label1.update()
        urgentcanvas.pack()
        labelj.pack()
        urgentcanvas.place(relx=0.5, rely=1, anchor=CENTER)
        labelj.place(relx=0.5, rely=0.85, anchor=CENTER)
        countdown(countdown_time)

    if e == 1:  # RESET BACK TO NORMAL MODE
        reseter()


menubar = tkinter.Menu(root)
filemenu = tkinter.Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=file1)
filemenu.add_separator()
filemenu.add_command(label="Open", command=openfile)
filemenu.add_separator()
filemenu.add_command(label="Save", command=savefile)
filemenu.add_command(label="Save as...", command=savefileas)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=on_closing)
filemenu.add_separator()
filemenu.add_checkbutton(label="Dont Make Transparent", onvalue=1, offvalue=0, variable=j)
filemenu.add_separator()
filemenu.add_command(label=version)
menubar.add_cascade(label="Options", menu=filemenu)

k = IntVar()
k.set(1)
filemenu = tkinter.Menu(menubar, tearoff=0)
filemenu.add_checkbutton(label="Notepad", onvalue=1, offvalue=1, variable=k, command=modes)
filemenu.add_checkbutton(label="Urgent", onvalue=2, offvalue=1, variable=k, command=modes)
filemenu.add_checkbutton(label="Reminder", onvalue=3, offvalue=1, variable=k, command=modes)
filemenu.add_checkbutton(label="TODO", onvalue=4, offvalue=1, variable=k, command=modes)
menubar.add_cascade(label="Type", menu=filemenu)

root.config(menu=menubar)
root.geometry("300x400")
root.resizable(False, False)  # makes it so that you cannot change the size of the window
root.protocol("WM_DELETE_WINDOW", on_closing)  # calls on_closing method when user clicks the X button or alt+f4
root.mainloop()



        #TODO   ⢀⡴⠑⡄⠀⠀⠀⠀⠀⠀⠀⣀⣀⣤⣤⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        #      ⠸⡇⠀⠿⡀⠀⠀⠀⣀⡴⢿⣿⣿⣿⣿⣿⣿⣿⣷⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        #      ⠀⠀⠀⠀⠑⢄⣠⠾⠁⣀⣄⡈⠙⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀
        #      ⠀⠀⠀⠀⢀⡀⠁⠀⠀⠈⠙⠛⠂⠈⣿⣿⣿⣿⣿⠿⡿⢿⣆⠀⠀⠀⠀⠀⠀⠀
        #     ⠀⠀⠀⢀⡾⣁⣀⠀⠴⠂⠙⣗⡀⠀⢻⣿⣿⠭⢤⣴⣦⣤⣹⠀⠀⠀⢀⢴⣶⣆
        #      ⠀⢀⣾⣿⣿⣿⣷⣮⣽⣾⣿⣥⣴⣿⣿⡿⢂⠔⢚⡿⢿⣿⣦⣴⣾⠁⠸⣼⡿
        #      ⠀⢀⡞⠁⠙⠻⠿⠟⠉⠀⠛⢹⣿⣿⣿⣿⣿⣌⢤⣼⣿⣾⣿⡟⠉⠀⠀⠀⠀⠀
        #      ⠀⣾⣷⣶⠇⠀⠀⣤⣄⣀⡀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀
        #      ⠀⠉⠈⠉⠀⠀⢦⡈⢻⣿⣿⣿⣶⣶⣶⣶⣤⣽⡹⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀
        #      ⠀⠀⠀⠀⠀⠀⠀⠉⠲⣽⡻⢿⣿⣿⣿⣿⣿⣿⣷⣜⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀
        #      ⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣷⣶⣮⣭⣽⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀
        #      ⠀⠀⠀⠀⠀⠀⣀⣀⣈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀
        #      ⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀
        #      ⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
        #      ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠻⠿⠿⠿⠿⠛⠉     Shrek my beloved
