from tkinter import *
from tkinter import messagebox,ttk
import sqlite3

# WHEN USER CLICK ON LOGIN BUTTON
def Login_window():
    login_win = Toplevel(win)
    login_win.title("User Login")
    login_win.geometry("300x300")
    login_win.config(bg="light gray")

    lab_heading = Label(login_win, text="Login Page", bg="gray", fg="white", font=("Arial", 14, "bold"))
    lab_heading.grid(row=0, column=0, columnspan=2, padx=20, pady=20)

    lab_user = Label(login_win, text="Username:", bg="light gray", font=("Arial", 12))
    lab_user.grid(row=1, column=0, padx=10, pady=10)
    ent1 = Entry(login_win, width=25)
    ent1.grid(row=1, column=1, padx=10, pady=10)

    lab_pass = Label(login_win, text="Password:", bg="light gray", font=("Arial", 12))
    lab_pass.grid(row=2, column=0, padx=10, pady=10)
    ent2 = Entry(login_win, show='*', width=25)
    ent2.grid(row=2, column=1, padx=10, pady=10)

    def show_popup():
        messagebox.showinfo("login status", "Login successfully!")
    button3 = Button(login_win, text="SUBMIT", bd=5, command=show_popup)
    button3.grid(row=3, column=1, pady=20, sticky='e')
def Register_window():
    register_win = Toplevel(win)
    register_win.title("User Registration")
    register_win.geometry("400x400")
    register_win.config(bg="light gray")

    lab_heading2 = Label(register_win, text="Registration Page", bg="gray", fg="white", font=("Arial", 14, "bold"))
    lab_heading2.grid(row=0, column=0, columnspan=2, padx=20, pady=20)

    reg_fullname= Label(register_win,text="Full name",bg="light grey", font=("Arial",12))
    reg_fullname.grid(row=1, column=0, padx=10, pady=10)
    ent3 = Entry(register_win, width=25)
    ent3.grid(row=1, column=1, padx=10, pady=10)

    reg_user=Label(register_win,text=" Register Username:", bg="light gray", font=("Arial", 12))
    reg_user.grid(row=2, column=0, padx=10, pady=10)
    ent4 = Entry(register_win, width=25)
    ent4.grid(row=2, column=1, padx=10, pady=10)

    reg_email = Label(register_win,text="Email:", bg="light gray", font=("Arial",12))
    reg_email.grid(row=3, column=0, padx=10, pady=10)
    ent5 = Entry(register_win,  width=25)
    ent5.grid(row=3, column=1, padx=10, pady=10)

    reg_pass = Label(register_win, text="Password:", bg="light gray", font=("Arial", 12))
    reg_pass.grid(row=4, column=0, padx=10, pady=10)
    ent6 = Entry(register_win, show='*', width=25)
    ent6.grid(row=4, column=1, padx=10, pady=10)

    def show_registered_popup():
        fullname = ent3.get()
        username = ent4.get()
        email = ent5.get()
        password = ent6.get()

        if fullname and username and email and password:
            conn = sqlite3.connect('users.db')
            cur = conn.cursor()
            cur.execute("INSERT INTO register (fullname, username, email, password) VALUES (?, ?, ?, ?)",
                        (fullname, username, email, password))
            conn.commit()
            conn.close()
            messagebox.showinfo("Registration Status", "Registered successfully!")
            ent3.delete(0, END)
            ent4.delete(0, END)
            ent5.delete(0, END)
            ent6.delete(0, END)
        else:
            messagebox.showwarning("Input Error", "All fields are required.")

    Button(register_win, text="Register", bd=5, command=show_registered_popup).grid(row=5, column=1, pady=20, sticky='e')


def admin_login():
    admin_lo = Toplevel(win)
    admin_lo.title("Admin Login")
    admin_lo.geometry("400x300")
    admin_lo.config(bg="light gray")

    Label(admin_lo, text="Admin Login", bg="gray", fg="white", font=("Arial", 14, "bold")).pack(pady=10)
    Label(admin_lo, text="Username:", bg="light gray", font=("Arial", 12)).pack(pady=5)
    user_entry = Entry(admin_lo, width=25)
    user_entry.pack(pady=5)
    Label(admin_lo, text="Password:", bg="light gray", font=("Arial", 12)).pack(pady=5)
    pass_entry = Entry(admin_lo, show='*', width=25)
    pass_entry.pack(pady=5)

    def admin_check():
        username = user_entry.get()
        password = pass_entry.get()
        if username == "admin" and password == "1234":
            messagebox.showinfo(" Admin Login Successfully", "Login successfully!")
            admin_lo.destroy()
            open_crud_window()
        else:
            messagebox.showerror(" Admin Login Failed", "Login Failed!")
    Button(admin_lo, text="Login", command=admin_check, bd=5).pack(pady=20)

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS register (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT,
            username TEXT,
            email TEXT,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def open_crud_window():
    crud_win = Toplevel(win)
    crud_win.title("Manage Users (CRUD)")
    crud_win.geometry("600x400")

    tree = ttk.Treeview(crud_win, columns=("id", "fullname", "username", "email", "password"), show="headings")
    tree.heading("id", text="ID")
    tree.heading("fullname", text="Full Name")
    tree.heading("username", text="Username")
    tree.heading("email", text="Email")
    tree.heading("password", text="Password")
    tree.pack(fill=BOTH, expand=True)

    def load_data():
        for i in tree.get_children():
            tree.delete(i)
        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM register")
        rows = cur.fetchall()
        for row in rows:
            tree.insert("", END, values=row)
        conn.close()

    def delete_record():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Error", "Select a record to delete.")
            return
        item = tree.item(selected)
        user_id = item['values'][0]
        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        cur.execute("DELETE FROM register WHERE id=?", (user_id,))
        conn.commit()
        conn.close()
        load_data()

    Button(crud_win, text="Refresh", command=load_data).pack(side=LEFT, padx=10, pady=10)
    Button(crud_win, text="Delete", command=delete_record).pack(side=LEFT, padx=10, pady=10)
    load_data()

win = Tk()
win.title("Login Form")
win.minsize(width=500, height=400)
win.config(background="white")

lab = Label(win, text="*** SECURE USER AND ADMIN DASHBOARD ***", bg="black", fg="white", font=("Arial", 14, "bold"))
lab.grid(row=0, column=0, columnspan=2, padx=20, pady=29)

button0 = Button(win, text="LOGIN", bd=10, command=Login_window)
button0.grid(row=1, column=0, pady=20, sticky='e')
button1 = Button(win, text="REGISTER", bd=10, command=Register_window)
button1.grid(row=2, column=0, pady=20, sticky='e')
button2 = Button(win, text="ADMIN LOGIN", bd=10,command=admin_login)
button2.grid(row=3, column=0, pady=20, sticky='e')

win.mainloop()
