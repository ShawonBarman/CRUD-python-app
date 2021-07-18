from tkinter import *
from tkinter import messagebox
from sqlserver_config import dbconfig   #that contains the configuration details to connect to our server.
import pypyodbc   #first install this module by using that command : pip install pypyodbc

#create a variable for the connection, ant the connection to be stored inside the variable.
con = pypyodbc.connect(**dbconfig)

cursor = con.cursor()  #this is allow our python code to interact with the database and execute commands within a database session because objects can be created by using the connect.cursor method.

class Bookdb:
    def __init__(self):
        self.con = pypyodbc.connect(**dbconfig)
        self.cursor = con.cursor()
        print("You have connected to the database.")
        print(con)

    def __del__(self):
        self.con.close()

    def view(self):
        self.cursor.execute("SELECT * FROM books")
        row = self.cursor.fetchall()
        return row

    #for insert new data into database
    def insert(self, title, author, ISBN):
        sql = ("INSERT INTO books(title, author, ISBN) VALUES(?, ?, ?)")
        value = [title, author, ISBN]
        self.cursor.execute(sql, value)
        self.con.commit()
        messagebox.showinfo(title="Book Database", message="New book added to database")

    #for modify the specific data from database
    def update(self, id, title, author, isbn):
        tsql = 'UPDATE books SET  title = ?, author = ?, isbn = ? WHERE id=?'
        self.cursor.execute(tsql, [title,author,isbn,id])
        self.con.commit()
        messagebox.showinfo(title="Book Database",message="Book Updated")

    #for delete the specific data from database
    def delete(self, id):
        defquery = "DELETE FROM books WHERE id = ?"
        self.cursor.execute(defquery, [id])
        self.con.commit()
        messagebox.showinfo(title="Book database", message="Delete book")

db = Bookdb()

#for select the data into our listbox
def get_selected_row(event):
    global selected_tuple
    index = list_bx.curselection()[0]
    selected_tuple = list_bx.get(index)
    title_entry.delete(0, 'end')
    title_entry.insert('end', selected_tuple[1])
    author_entry.delete(0, 'end')
    author_entry.insert('end', selected_tuple[2])
    isbn_entry.delete(0, 'end')
    isbn_entry.insert('end', selected_tuple[3])

#this method is for show all data by clicking the view_btn button
def view_record():
    list_bx.delete(0, 'end')
    for row in db.view():
        list_bx.insert('end', row)

#this method is for add new data by clicking the add_btn button
def add_book():
    db.insert(title_text.get(), author_text.get(), isbn_text.get())
    list_bx.delete(0, 'end')
    list_bx.insert('end', (title_text.get(), author_text.get(), isbn_text.get()))
    title_entry.delete(0, 'end')
    author_entry.delete(0, 'end')
    isbn_entry.delete(0, 'end')
    con.commit()

#this method is for delete data by clicking the delete_btn button
def delete_records():
    db.delete(selected_tuple[0])
    con.commit()

#this method is for clear all data into our listbox by clicking the clear_btn button
def clear_screen():
    list_bx.delete(0, 'end')
    title_entry.delete(0, 'end')
    author_entry.delete(0, 'end')
    isbn_entry.delete(0, 'end')

#this method is for update data by clicking the modify_btn button
def update_records():
    db.update(selected_tuple[0], title_text.get(), author_text.get(), isbn_text.get())
    title_entry.delete(0, 'end')
    author_entry.delete(0, 'end')
    isbn_entry.delete(0, 'end')
    con.commit()

#this method is for exit application by clicking the exit_btn button
def on_closing():
    dd = db
    if messagebox.askokcancel("Quit", "Do you want to quit:"):
        root.destroy()
        del dd

root = Tk()    #create application window

root.title("My books database application")    #add a title to application window
root.configure(background="light green")    #add background color to application window
root.geometry("875x525")    #sets a size for application window
root.resizable(width=False, height=False)    #prevents the application window from resizing

#create labels and entry widgets
Label(root, text="Title", padx=15, pady=10, background="light green", font=("TKDefaultFont", 16)).grid(row=0, column=0, sticky=W)
title_text = StringVar()
title_entry = Entry(root, width = 24,textvariable = title_text)
title_entry.grid(row=0, column=1, sticky=W)

title_label = Label(root, text="Author", padx=15, pady=10, background="light green", font=("TKDefaultFont", 16))
title_label.grid(row=0, column=2, sticky=W)
author_text = StringVar()
author_entry = Entry(root, width = 24,textvariable = author_text)
author_entry.grid(row=0, column=3, sticky=W)

title_label = Label(root, text="ISBN", padx=15, pady=10, background="light green", font=("TKDefaultFont", 16))
title_label.grid(row=0, column=4, sticky=W)
isbn_text = StringVar()
isbn_entry = Entry(root, width = 24,textvariable = isbn_text)
isbn_entry.grid(row=0, column=5, sticky=W)

#add a button to insert inputs into database
add_btn = Button(root, text="Add Book", padx=5, pady=5, bg="blue", fg="white", font="helvetica 10 bold", command=add_book)
add_btn.grid(row=0, column=7, sticky=W)

#add a listbox to display data from database
list_bx = Listbox(root, height=16, width=45, font="helvetica 13", bg="light blue")
list_bx.grid(row=3, column=1, columnspan=14, sticky=W+E, pady=40, padx=15)
list_bx.bind('<<ListboxSelect>>', get_selected_row)

#add scrollbar to enable scrolling
scroll_bar = Scrollbar(root)
scroll_bar.grid(row=1, column=8, rowspan=14, sticky=W)

list_bx.configure(yscrollcommand=scroll_bar.set)  #enable vertical scorlling
scroll_bar.configure(command=list_bx.yview)

#add more button widgets
modify_btn = Button(root, text="Modify record", bg="purple", fg="white", font="helvetica 10 bold", command=update_records)
modify_btn.grid(row=15, column=4)

delete_btn = Button(root, text="Delete record", bg="red", fg="white", font="helvetica 10 bold", command=delete_records)
delete_btn.grid(row=15, column=5)

view_btn = Button(root, text="View all records", bg="black", fg="white", font="helvetica 10 bold", command=view_record)
view_btn.grid(row=15, column=1)

clear_btn = Button(root, text="CLear Screen", bg="maroon", fg="white", font="helvetica 10 bold", command=clear_screen)
clear_btn.grid(row=15, column=2)

exit_btn = Button(root, text="Exit Application", bg="dark blue", fg="white", font="helvetica 10 bold", command=on_closing)
exit_btn.grid(row=15, column=3)

root.mainloop()