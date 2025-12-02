from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import ttkthemes, time

from database import connect_to_mysql, setup_database
from student_functions import add_student, update_student, delete_student, fetch_all_students, export_data

# --- Database ---
con = setup_database()
if con:
    cursor = con.cursor()

# --- Helper Functions ---

def refresh_student_table():
    studentTable.delete(*studentTable.get_children())
    students = fetch_all_students(cursor)
    for student in students:
        studentTable.insert('', END, values=student)

# --- Login / Signup Functions ---

def login():
    username = usernameEntry.get()
    password = passwordEntry.get()
    if username == '' or password == '':
        messagebox.showerror('Error', 'Fields cannot be empty')
        return

    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()
    if user:
        messagebox.showinfo('Success', f'Welcome {username}')
        login_frame.pack_forget()
        student_frame.pack(fill=BOTH, expand=1)
        refresh_student_table()
    else:
        messagebox.showerror('Error', 'Incorrect credentials')

def signup():
    username = usernameEntry.get()
    password = passwordEntry.get()
    email = emailEntry.get()
    if username == '' or password == '' or email == '':
        messagebox.showerror('Error', 'All fields required')
        return

    try:
        cursor.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)", 
                       (username, password, email))
        con.commit()
        messagebox.showinfo('Success', 'Sign up successful. Please login.')
    except Exception as e:
        messagebox.showerror('Error', f'Sign up failed: {e}')

def forgot_password():
    messagebox.showinfo('Forgot Password', 'Please contact support to reset your password.')

# --- GUI Setup ---

root = ttkthemes.ThemedTk()
root.set_theme('radiance')
root.geometry('1280x700')
root.resizable(False, False)
root.title('Teacher Management System')

# --- Login Frame ---
login_frame = Frame(root, bg='white')
login_frame.pack(fill=BOTH, expand=1)

# Background Image
bg_img = Image.open("images/image1.jpg").resize((1280, 700))
bg_photo = ImageTk.PhotoImage(bg_img)
bg_label = Label(login_frame, image=bg_photo)
bg_label.place(x=0, y=0)

# Login Box
login_box = Frame(login_frame, bg='white')
login_box.place(x=400, y=150)

# Logo
logo_img = Image.open("images/logo.png").resize((50,50))
logo_photo = ImageTk.PhotoImage(logo_img)
Label(login_box, image=logo_photo, bg='white').grid(row=0, column=0, columnspan=2, pady=10)

# Username
Label(login_box, text='Username', font=('times new roman', 20, 'bold'), bg='white').grid(row=1, column=0, pady=10, padx=20)
usernameEntry = Entry(login_box, font=('times new roman', 20, 'bold'), bd=5, fg='royalblue')
usernameEntry.grid(row=1, column=1, pady=10, padx=20)

# Password
Label(login_box, text='Password', font=('times new roman', 20, 'bold'), bg='white').grid(row=2, column=0, pady=10, padx=20)
passwordEntry = Entry(login_box, font=('times new roman', 20, 'bold'), bd=5, fg='royalblue', show='*')
passwordEntry.grid(row=2, column=1, pady=10, padx=20)

# Email (Signup only)
Label(login_box, text='Email', font=('times new roman', 20, 'bold'), bg='white').grid(row=3, column=0, pady=10, padx=20)
emailEntry = Entry(login_box, font=('times new roman', 20, 'bold'), bd=5, fg='royalblue')
emailEntry.grid(row=3, column=1, pady=10, padx=20)

# Buttons
Button(login_box, text='Login', font=('times new roman', 14, 'bold'), width=15, 
       fg='white', bg='cornflowerblue', command=login).grid(row=4, column=1, pady=10)
Button(login_box, text='Sign Up', font=('times new roman', 14, 'bold'), width=15, 
       fg='white', bg='green', command=signup).grid(row=4, column=0, pady=10)
Button(login_box, text='Forgot Password?', font=('times new roman', 12), fg='blue', bg='white',
       bd=0, command=forgot_password).grid(row=5, columnspan=2, pady=10)

# --- Student Management Frame ---
student_frame = Frame(root)
# Initially hidden, only shown after login

# Left Frame - Buttons
leftFrame = Frame(student_frame)
leftFrame.pack(side=LEFT, padx=20, pady=20, fill=Y)

Button(leftFrame, text='Add Student', width=20).pack(pady=10)
Button(leftFrame, text='Update Student', width=20).pack(pady=10)
Button(leftFrame, text='Delete Student', width=20).pack(pady=10)
Button(leftFrame, text='Export Data', width=20, command=lambda: export_data(studentTable)).pack(pady=10)

''' Logout button for user '''
def logout():
    student_frame.pack_forget()
    login_frame.pack(fill=BOTH, expand=1)
Button(leftFrame, text='Logout', width=20, bg='red', fg='white', command=logout).pack(pady=10)

# Right Frame - Table
rightFrame = Frame(student_frame)
rightFrame.pack(side=LEFT, padx=10, pady=20)

studentTable = ttk.Treeview(rightFrame, columns=('Id', 'Name', 'Mobile', 'Email', 'Address', 'Gender', 'D.O.B', 'Added Date', 'Added Time'),
                            show='headings', height=20)
for col in studentTable["columns"]:
    studentTable.heading(col, text=col)
    studentTable.column(col, width=100, anchor=CENTER)

studentTable.pack(expand=1, fill=BOTH)

# --- Run the GUI ---
root.mainloop()
