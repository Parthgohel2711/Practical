from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector

con = mysql.connector.connect(host="localhost", user="root", password="", autocommit=True)
cur = con.cursor()
cur.execute("CREATE DATABASE IF NOT EXISTS studentdb")
cur.execute("USE studentdb")
cur.execute("CREATE TABLE IF NOT EXISTS students(id INT PRIMARY KEY AUTO_INCREMENT, username VARCHAR(100), age INT, course VARCHAR(50), gender VARCHAR(10))")

CrudPage = Tk()
CrudPage.title("Crud Operation Page")
CrudPage.geometry("700x480")
CrudPage.resizable(False, False)

main_font = ("Times New Roman", 14)

Label(CrudPage, text="Enter Username", font=main_font).place(x=20, y=20)
Label(CrudPage, text="Enter Your Age", font=main_font).place(x=20, y=60)
Label(CrudPage, text="Enter Your Course", font=main_font).place(x=20, y=100)
Label(CrudPage, text="Select Gender", font=main_font).place(x=20, y=140)

Entry_Username = Entry(CrudPage, font=main_font)
Entry_Username.place(x=220, y=20)

Entry_Age = Entry(CrudPage, font=main_font)
Entry_Age.place(x=220, y=60)

selected_option = StringVar()
options = ["Bca", "Bscit", "Bba", "Bcom", "Bsw", "Ba"]
combobox_Course = ttk.Combobox(CrudPage, textvariable=selected_option, values=options, width=28, font=main_font)
combobox_Course.set(options[0])
combobox_Course['state'] = 'readonly'
combobox_Course.place(x=220, y=100)

Radio_var = StringVar()
Radio_var.set("Male")

Radiobutton(CrudPage, variable=Radio_var, text="Male", value="Male", font=main_font).place(x=220, y=140)
Radiobutton(CrudPage, variable=Radio_var, text="Female", value="Female", font=main_font).place(x=300, y=140)

tree_frame = Frame(CrudPage)
tree_frame.place(x=20, y=220, width=660, height=240)

scroll_y = Scrollbar(tree_frame, orient=VERTICAL)
scroll_x = Scrollbar(tree_frame, orient=HORIZONTAL)

tree = ttk.Treeview(
    tree_frame,
    columns=("id", "username", "age", "course", "gender"),
    show="headings",
    yscrollcommand=scroll_y.set,
    xscrollcommand=scroll_x.set
)

scroll_y.config(command=tree.yview)
scroll_x.config(command=tree.xview)

scroll_y.pack(side=RIGHT, fill=Y)
scroll_x.pack(side=BOTTOM, fill=X)

tree.heading("id", text="ID")
tree.heading("username", text="Username")
tree.heading("age", text="Age")
tree.heading("course", text="Course")
tree.heading("gender", text="Gender")

tree.column("id", width=50, anchor=CENTER)
tree.column("username", width=180)
tree.column("age", width=80, anchor=CENTER)
tree.column("course", width=160)
tree.column("gender", width=100, anchor=CENTER)

style = ttk.Style()
style.configure("Treeview", font=main_font, rowheight=28)
style.configure("Treeview.Heading", font=("Times New Roman", 15, "bold"))

tree.pack(expand=True, fill=BOTH)

selected_id = None

def set_button_state(btn, state):
    if state == "normal":
        if btn == btn_insert:
            btn.config(bg="#4CAF50", fg="white")
        elif btn == btn_update:
            btn.config(bg="#6EC6FF", fg="black")
        elif btn == btn_delete:
            btn.config(bg="#f44336", fg="white")
        else:
            btn.config(bg="#6EC6FF", fg="black")
    else:
        btn.config(bg="#BDBDBD", fg="white")
    btn.config(state=state)

def refresh_tree():
    for i in tree.get_children():
        tree.delete(i)
    cur.execute("SELECT * FROM students")
    for row in cur.fetchall():
        tree.insert("", END, values=row)

def clear_fields_and_reset():
    global selected_id
    selected_id = None
    Entry_Username.delete(0, END)
    Entry_Age.delete(0, END)
    combobox_Course.set(options[0])
    Radio_var.set("Male")

    set_button_state(btn_insert, "normal")
    set_button_state(btn_update, "disabled")
    set_button_state(btn_delete, "disabled")

    tree.selection_remove(tree.selection())

def on_tree_select(event):
    global selected_id
    sel = tree.selection()
    if not sel:
        return
    item = tree.item(sel[0])
    vals = item.get("values")
    if not vals:
        return

    selected_id = vals[0]

    Entry_Username.delete(0, END)
    Entry_Age.delete(0, END)

    Entry_Username.insert(0, vals[1])
    Entry_Age.insert(0, vals[2])
    combobox_Course.set(vals[3])
    Radio_var.set(vals[4])

    set_button_state(btn_update, "normal")
    set_button_state(btn_delete, "normal")
    set_button_state(btn_insert, "disabled")

def insert_data():
    u = Entry_Username.get().strip()
    a = Entry_Age.get().strip()
    c = selected_option.get()
    g = Radio_var.get()

    if u == "" or a == "":
        messagebox.showerror("Error", "Username and Age are required")
        return

    try:
        ai = int(a)
    except:
        messagebox.showerror("Error", "Age must be a number")
        return

    cur.execute("INSERT INTO students(username, age, course, gender) VALUES(%s,%s,%s,%s)", (u, ai, c, g))
    refresh_tree()
    clear_fields_and_reset()

def update_data():
    global selected_id
    if not selected_id:
        return

    u = Entry_Username.get().strip()
    a = Entry_Age.get().strip()
    c = selected_option.get()
    g = Radio_var.get()

    if u == "" or a == "":
        messagebox.showerror("Error", "Username and Age are required")
        return

    try:
        ai = int(a)
    except:
        messagebox.showerror("Error", "Age must be a number")
        return

    cur.execute("UPDATE students SET username=%s, age=%s, course=%s, gender=%s WHERE id=%s", (u, ai, c, g, selected_id))
    refresh_tree()
    clear_fields_and_reset()

def delete_data():
    global selected_id
    if not selected_id:
        return

    if not messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this record?"):
        return

    cur.execute("DELETE FROM students WHERE id=%s", (selected_id,))
    refresh_tree()
    clear_fields_and_reset()

btn_insert = Button(CrudPage, text="Insert", width=12, font=main_font, command=insert_data)
btn_update = Button(CrudPage, text="Update", width=12, font=main_font, command=update_data)
btn_delete = Button(CrudPage, text="Delete", width=12, font=main_font, command=delete_data)
btn_clear = Button(CrudPage, text="Clear", width=12, font=main_font, bg="#6EC6FF", fg="black", command=clear_fields_and_reset)

btn_insert.place(x=160, y=170)
btn_update.place(x=300, y=170)
btn_delete.place(x=440, y=170)
btn_clear.place(x=20, y=170)

tree.bind("<<TreeviewSelect>>", on_tree_select)

refresh_tree()
clear_fields_and_reset()

CrudPage.mainloop()
