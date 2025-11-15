import mysql.connector as sql
import tkinter as tk
from tkinter import messagebox

class login:
    def conn(self):
        self.con = sql.connect(host="localhost", user="root", password="")
        self.cur = self.con.cursor()
        self.cur.execute("CREATE DATABASE IF NOT EXISTS log")
        self.con.database = "log"
        self.cur.execute("CREATE TABLE IF NOT EXISTS log_tbl (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(40), password VARCHAR(40))")
        self.con.commit()
        
    def login(self):
        self.conn()
        name = E_name.get()
        password = E_password.get()
        self.cur.execute("SELECT * FROM log_tbl WHERE name=%s AND password=%s", (name, password))
        row = self.cur.fetchone()
        if row:
            messagebox.showinfo("Login", "Login Successful")
        else:
            messagebox.showerror("Login", "Invalid Username or Password")
        self.con.close()
        
log = login()
Loginpage = tk.Tk()
Loginpage.geometry("470x200")
Loginpage.title("Login Page")

name = tk.Label(Loginpage, text="Enter Username", font=("TimesNewRoman"))
name.place(x=20, y=20)
password = tk.Label(Loginpage, text="Enter Password", font=("TimesNewRoman"))
password.place(x=20, y=60)

E_name = tk.Entry(Loginpage, font=("TimesNewRoman"))
E_name.place(x=200, y=20)
E_password = tk.Entry(Loginpage, font=("TimesNewRoman"), show="*")
E_password.place(x=200, y=60)

button = tk.Button(Loginpage, text="Login", font=("TimesNewRoman"), width="34", bg="skyblue", command=log.login)
button.place(x=20, y=100)

Loginpage.mainloop()
