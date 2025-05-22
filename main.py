                          # Main window of our lbms 

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from functions import add_book, search_book, delete_book, update_book, add_user, search_user, delete_user, update_user, issue_book, book_return, fetch_all_books, fetch_all_users, fetch_all_issued_books
import datetime
from dbconnector import connect_db                       
                       
                        # Function related to books table

# Function to open the Add Book window

def open_add_book():
    add_book_window = tk.Toplevel()
    add_book_window.title("Add Book")
    add_book_window.geometry("400x550")
    add_book_window.configure(bg="#E2EAF4")   

    # Labels and Entry Fields
    tk.Label(add_book_window, text="Book ID", font=("Arial", 12), bg="#E2EAF4").pack(pady=5)
    book_id_entry = tk.Entry(add_book_window, font=("Arial", 12))
    book_id_entry.pack(pady=5)

    tk.Label(add_book_window, text="Title", font=("Arial", 12), bg="#E2EAF4").pack(pady=5)
    title_entry = tk.Entry(add_book_window, font=("Arial", 12))
    title_entry.pack(pady=5)

    tk.Label(add_book_window, text="Author", font=("Arial", 12), bg="#E2EAF4").pack(pady=5)
    author_entry = tk.Entry(add_book_window, font=("Arial", 12))
    author_entry.pack(pady=5)

    
    tk.Label(add_book_window, text="Genre", font=("Arial", 12), bg="#E2EAF4").pack(pady=5)
    genre_entry = tk.Entry(add_book_window, font=("Arial", 12))
    genre_entry.pack(pady=5)

    tk.Label(add_book_window, text="Publish Year", font=("Arial", 12), bg="#E2EAF4").pack(pady=5)
    publish_year_entry = tk.Entry(add_book_window, font=("Arial", 12))
    publish_year_entry.pack(pady=5)

    tk.Label(add_book_window, text="Copies Available", font=("Arial", 12), bg="#E2EAF4").pack(pady=5)
    copies_available_entry = tk.Entry(add_book_window, font=("Arial", 12))
    copies_available_entry.pack(pady=5)

    # Submit button
    def submit_book():
        Book_id = book_id_entry.get()
        Title = title_entry.get()
        Author = author_entry.get()
        Genre = genre_entry.get()
        Publish_year = publish_year_entry.get()
        Copies_Available = copies_available_entry.get()

        if not (Book_id and Title and Author and Genre and Publish_year and Copies_Available):
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            Publish_year_int = int(Publish_year)
            Copies_Available_int = int(Copies_Available)

            print("Submitting book...")
            add_book(Book_id, Title, Author, Genre, Publish_year_int, Copies_Available_int)
            messagebox.showinfo("Success", "Book added successfully.")
            add_book_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add book: {e}")
    
    tk.Button(add_book_window, text="Submit", font=("Arial", 12), bg="#4CAF50", fg="white", command=submit_book).pack(pady=20)


# Function to open the View Books window

def open_view_books():
    view_books_window = tk.Toplevel()
    view_books_window.title("View Books")
    view_books_window.geometry("800x400")
    view_books_window.configure(bg="#E2EAF4")

    # Title label
    tk.Label(view_books_window, text="Books List", font=("Arial", 16, "bold"), bg="#E2EAF4").pack(pady=10)

    columns = ("Book_ID", "Title", "Author", "Genre", "Publish_year", "Copies_available", "Status")
    tree = ttk.Treeview(view_books_window, columns=columns, show='headings')

    for col in columns:
        tree.heading(col, text=col.replace("_", " "))
        tree.column(col, width=100, anchor='center')

    tree.pack(fill=tk.BOTH, expand=True, pady=20, padx=20)

    books = fetch_all_books()
    for book in books:
        tree.insert("", tk.END, values=book)

    # Adding vertical scrollbar
    scrollbar = ttk.Scrollbar(view_books_window, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    close_btn = tk.Button(view_books_window, text="Close", command=view_books_window.destroy, font=("Arial", 12), bg="#4CAF50", fg="white")
    close_btn.pack(pady=10)

# Function to open the Search book window

def open_search_book():
    search_book_window = tk.Toplevel()
    search_book_window.title("Search Book")
    search_book_window.geometry("800x400")
    search_book_window.configure(bg="#E2EAF4")

    form_frame = tk.Frame(search_book_window, bg="#E2EAF4")
    form_frame.pack(pady=10)

    # Label and Entry for Title
    tk.Label(form_frame, text="Enter Book Title:", font=("Arial", 12), bg="#E2EAF4").pack(pady=5)
    title_entry = tk.Entry(form_frame, font=("Arial", 12))
    title_entry.pack(pady=5)

    tree = None
    scrollbar = None

    def reset_to_search():
        nonlocal tree, scrollbar
        if tree:
            tree.destroy()
        if scrollbar:
            scrollbar.destroy()
        search_book_window.title("Search Book")
        form_frame.pack(pady=30)
        back_button.pack_forget()

    # Submit button
    def submit_book():
        nonlocal tree, scrollbar
        title = title_entry.get()

        if not title:
            messagebox.showerror("Error", "Title field is required")
            return

        try:
            books = search_book(title) 
            if not books:
                messagebox.showinfo("Not Found", "Book not found.")
                return
            
            search_book_window.title(f"Search Results for '{title}'") 
            form_frame.pack_forget()  

            columns = ("Book ID","Title", "Author", "Genre", "Publish Year", "Copies Available")
            tree = ttk.Treeview(search_book_window, columns=columns, show='headings')

            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=140, anchor='center')

            for book in books:
                tree.insert("", tk.END, values=book)

            tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

            # Adding scrollbar
            scrollbar = ttk.Scrollbar(search_book_window, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscroll=scrollbar.set)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            back_button.pack(pady=10)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to find book: {e}")

    tk.Button(form_frame, text="Search", font=("Arial", 12), bg="#4CAF50", fg="white", command=submit_book).pack(pady=10)
    back_button = tk.Button(search_book_window, text="Back to Search", font=("Arial", 12), bg="#2196F3", fg="white", command=reset_to_search)


# Function to open the Delete Book window

def open_delete_book():
    delete_book_window = tk.Toplevel()
    delete_book_window.title("Delete Book")
    delete_book_window.geometry("400x200")
    delete_book_window.configure(bg="#E2EAF4")
    
    tk.Label(delete_book_window, text="Enter Book ID", font=("Arial", 12), bg="#FBE9E7").pack(pady=20)
    book_id_entry = tk.Entry(delete_book_window, font=("Arial", 12))
    book_id_entry.pack(pady=10)

    def delete_action():
        book_id = book_id_entry.get().strip()

        if not book_id:
            messagebox.showerror("Error", "Book ID is required.")
            return

        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete Book ID {book_id}?")
        if not confirm:
            return

        success, message = delete_book(book_id)
        if success:
            messagebox.showinfo("Success", message)
            delete_book_window.destroy()
        else:
            messagebox.showerror("Error", message)

    tk.Button(delete_book_window, text="Delete", font=("Arial", 12), bg="#E53935", fg="white", command=delete_action).pack(pady=20)


# Function to open the Update book window

def open_update_book():  
    update_book_window = tk.Toplevel()
    update_book_window.title("Update Book")
    update_book_window.geometry("400x550")
    update_book_window.configure(bg="#E2EAF4")

    # Labels and Entry Fields
    entries = {}
    fields = ["Book ID", "Title", "Author", "Genre", "Publish Year", "Copies Available"]
    
    for field in fields:
        tk.Label(update_book_window, text=field, font=("Arial", 12), bg="#E2EAF4").pack(pady=5)
        entry = tk.Entry(update_book_window, font=("Arial", 12))
        entry.pack(pady=5)
        entries[field] = entry

    # Submit button 
    def submit_update():
        values = {field: entries[field].get() for field in fields}
        
        if not all(values.values()):
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            update_book(
                values["Book ID"],
                values["Title"],
                values["Author"],
                values["Genre"],
                values["Publish Year"],
                values["Copies Available"]
            )
            messagebox.showinfo("Success", "Updated successfully.")
            update_book_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update: {e}")

    tk.Button(update_book_window, text="Update", font=("Arial", 12), bg="#4CAF50", fg="white", command=submit_update).pack(pady=20)            


# Function to open the Issue Book window

def open_issue_book():
    issue_book_window = tk.Toplevel()
    issue_book_window.title("Issue Book")
    issue_book_window.geometry("400x550")
    issue_book_window.configure(bg="#E2EAF4")

    # Labels and Entry Fields
    tk.Label(issue_book_window, text="Issue ID", font=("Arial", 12), bg="#E2EAF4").pack(pady=5)
    issue_id_entry = tk.Entry(issue_book_window, font=("Arial", 12))
    issue_id_entry.pack(pady=5)

    tk.Label(issue_book_window, text="User ID", font=("Arial", 12), bg="#E2EAF4").pack(pady=5)
    user_id_entry = tk.Entry(issue_book_window, font=("Arial", 12))
    user_id_entry.pack(pady=5)

    tk.Label(issue_book_window, text="Book ID", font=("Arial", 12), bg="#E2EAF4").pack(pady=5)
    book_id_entry = tk.Entry(issue_book_window, font=("Arial", 12))
    book_id_entry.pack(pady=5)
    
    tk.Label(issue_book_window, text="Issue Date", font=("Arial", 12), bg="#E2EAF4").pack(pady=5)
    issue_date_entry = tk.Entry(issue_book_window, font=("Arial", 12))
    issue_date_entry.pack(pady=5)

    tk.Label(issue_book_window, text="Due Date", font=("Arial", 12), bg="#E2EAF4").pack(pady=5)
    due_date_entry = tk.Entry(issue_book_window, font=("Arial", 12))
    due_date_entry.pack(pady=5)

    # Submit button
    def submit_issue():
        Issue_id = issue_id_entry.get()
        User_id = user_id_entry.get()
        Book_id = book_id_entry.get()
        Issue_date = issue_date_entry.get()
        Due_date = due_date_entry.get()
       

        if not (Issue_id and User_id and Book_id and Issue_date and Due_date):
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            print("Submitting book...")
            issue_book(Issue_id, User_id, Book_id, Issue_date, Due_date)
            messagebox.showinfo("Success", "Book has been issued successfully.")
            issue_book_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to issue book: {e}")
    tk.Button(issue_book_window, text="Submit", font=("Arial", 12), bg="#4CAF50", fg="white", command=submit_issue).pack(pady=20)


# Function to view the Issued books window

def open_view_issued_books():
    view_issued_books_window = tk.Toplevel()
    view_issued_books_window.title("View Issued Books")
    view_issued_books_window.geometry("900x450")
    view_issued_books_window.configure(bg="#E2EAF4")

    tk.Label(view_issued_books_window, text="Issued Books List", font=("Arial", 16, "bold"), bg="#E2EAF4").pack(pady=10)

    columns = ("Issue_ID", "User_ID", "Book_ID", "Book_Title", "Issue_date", "Due_date")
    tree = ttk.Treeview(view_issued_books_window, columns=columns, show='headings')

    for col in columns:
        tree.heading(col, text=col.replace("_", " "))
        tree.column(col, width=100, anchor='center')

    tree.pack(fill=tk.BOTH, expand=True, pady=20, padx=20)

    books = fetch_all_issued_books()
    for book in books:
        tree.insert("", tk.END, values=book)

    scrollbar = ttk.Scrollbar(view_issued_books_window, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    close_btn = tk.Button(view_issued_books_window, text="Close", command=view_issued_books_window.destroy, font=("Arial", 12), bg="#4CAF50", fg="white")
    close_btn.pack(pady=10)


# Function to open the Return Book window

def open_return_book():
    return_book_window = tk.Toplevel()
    return_book_window.title("Return Book")
    return_book_window.geometry("400x500")
    return_book_window.configure(bg="#E2EAF4")

    tk.Label(return_book_window, text="User ID", font=("Arial", 12), bg="#E2EAF4").pack(pady=5)
    user_id_entry = tk.Entry(return_book_window, font=("Arial", 12))
    user_id_entry.pack(pady=5)

    tk.Label(return_book_window, text="Book ID", font=("Arial", 12), bg="#E2EAF4").pack(pady=5)
    book_id_entry = tk.Entry(return_book_window, font=("Arial", 12))
    book_id_entry.pack(pady=5)

    tk.Label(return_book_window, text="Return Date (YYYY-MM-DD)", font=("Arial", 12), bg="#E2EAF4").pack(pady=5)
    return_date_entry = tk.Entry(return_book_window, font=("Arial", 12))
    return_date_entry.pack(pady=5)

    fine_label = tk.Label(return_book_window, text="Fine: Rs. 0.00", font=("Arial", 12, "bold"), bg="#E2EAF4", fg="red")
    fine_label.pack(pady=10)

    def calculate_fine():
        try:
            return_date_str = return_date_entry.get()
            return_date = datetime.datetime.strptime(return_date_str, "%Y-%m-%d").date()
            Book_id = book_id_entry.get()
            User_id = user_id_entry.get()

            if not Book_id or not User_id:
                messagebox.showerror("Missing Info", "Please enter both Book ID and User ID.")
                return

            db = connect_db()
            cursor = db.cursor()

            cursor.execute("""
                SELECT Due_date FROM ISSUES
                WHERE Book_ID = %s AND User_ID = %s AND Status = 'Issued'
                ORDER BY Issue_date DESC LIMIT 1
            """, (Book_id, User_id))
            result = cursor.fetchone()

            if result:
                due_date = result[0]
                days_late = (return_date - due_date).days
                fine = max(0, days_late * 2)
                fine_label.config(text=f"Fine: Rs. {fine:.2f}")
            else:
                messagebox.showerror("Not Found", "No active issue found for this Book ID and User ID.")

            cursor.close()
            db.close()

        except ValueError:
            messagebox.showerror("Invalid Date", "Please enter date as YYYY-MM-DD.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to calculate fine: {e}")

    def submit_return():
        User_id = user_id_entry.get()
        Book_id = book_id_entry.get()
        Return_date = return_date_entry.get()

        if not all([User_id, Book_id, Return_date]):
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            book_return(User_id, Book_id, Return_date)
            return_book_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to return book: {e}")

    tk.Button(return_book_window, text="Calculate Fine", font=("Arial", 12), bg="#2196F3", fg="white", command=calculate_fine).pack(pady=10)
    tk.Button(return_book_window, text="Return Book", font=("Arial", 12), bg="#4CAF50", fg="white", command=submit_return).pack(pady=10)


                # Function related to library users table
                

# Function to open the Add User window

def open_add_user():
    add_user_window = tk.Toplevel()
    add_user_window.title("Add User")
    add_user_window.geometry("400x550")
    add_user_window.configure(bg="#E2EAF4")

    # Labels and Entry Fields
    tk.Label(add_user_window, text="User ID", font=("Arial", 12), bg="#E2EAF4").pack(pady=5)
    user_id_entry = tk.Entry(add_user_window, font=("Arial", 12))
    user_id_entry.pack(pady=5)

    tk.Label(add_user_window, text="Name", font=("Arial", 12), bg="#E2EAF4").pack(pady=5)
    name_entry = tk.Entry(add_user_window, font=("Arial", 12))
    name_entry.pack(pady=5)

    tk.Label(add_user_window, text="Phone Number", font=("Arial", 12), bg="#E2EAF4").pack(pady=5)
    phone_entry = tk.Entry(add_user_window, font=("Arial", 12))
    phone_entry.pack(pady=5)

    
    tk.Label(add_user_window, text="Email", font=("Arial", 12), bg="#E2EAF4").pack(pady=5)
    email_entry = tk.Entry(add_user_window, font=("Arial", 12))
    email_entry.pack(pady=5)

    tk.Label(add_user_window, text="Address", font=("Arial", 12), bg="#E2EAF4").pack(pady=5)
    address_entry = tk.Entry(add_user_window, font=("Arial", 12))
    address_entry.pack(pady=5)

    tk.Label(add_user_window, text="Signup Date", font=("Arial", 12), bg="#E2EAF4").pack(pady=5)
    signup_date_entry = tk.Entry(add_user_window, font=("Arial", 12))
    signup_date_entry.pack(pady=5)

    # Submit button
    def submit_user():
        User_id= user_id_entry.get()
        Name= name_entry.get()
        Phone_number= phone_entry.get()
        Email= email_entry.get()
        Address= address_entry.get()
        Signup_date = signup_date_entry.get()
        

        if not (User_id and Name and Phone_number and Email and Address and Signup_date):
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            print("Submitting user...")
            add_user(User_id, Name, Phone_number, Email, Address, Signup_date)
            messagebox.showinfo("Success", "User added successfully.")
            add_user_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add user: {e}")
    tk.Button(add_user_window, text="Submit", font=("Arial", 12), bg="#4CAF50", fg="white", command=submit_user).pack(pady=20)           


# Function to open the View Users window

def open_view_users():
    view_users_window = tk.Toplevel()
    view_users_window.title("View Users")
    view_users_window.geometry("800x400")
    view_users_window.configure(bg="#E2EAF4")

    # Title label
    tk.Label(view_users_window, text="Users List", font=("Arial", 16, "bold"), bg="#E2EAF4").pack(pady=10)

    columns = ("User_ID", "Name", "Phone_number", "Email", "Address","Signup_date")
    tree = ttk.Treeview(view_users_window, columns=columns, show='headings')

    for col in columns:
        tree.heading(col, text=col.replace("_", " "))
        tree.column(col, width=100, anchor='center')

    tree.pack(fill=tk.BOTH, expand=True)

    users = fetch_all_users()
    for users in users:
        tree.insert("", tk.END, values=users)

    # Adding vertical scrollbar
    scrollbar = ttk.Scrollbar(view_users_window, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    close_btn = tk.Button(view_users_window, text="Close", command=view_users_window.destroy, font=("Arial", 12), bg="#4CAF50", fg="white")
    close_btn.pack(pady=10)


# Function to open the Search User window

def open_search_user():
    search_user_window = tk.Toplevel()
    search_user_window.title("Search Book")
    search_user_window.geometry("800x400")
    search_user_window.configure(bg="#E2EAF4")

    form_frame = tk.Frame(search_user_window, bg="#E2EAF4")
    form_frame.pack(pady=10)

    # Label and Entry for Title
    tk.Label(form_frame, text="Enter user name:", font=("Arial", 12), bg="#E2EAF4").pack(pady=5)
    name_entry = tk.Entry(form_frame, font=("Arial", 12))
    name_entry.pack(pady=5)

    tree = None
    scrollbar = None

    def reset_to_search():
        nonlocal tree, scrollbar
        if tree:
            tree.destroy()
        if scrollbar:
            scrollbar.destroy()
        search_user_window.title("Search User")
        form_frame.pack(pady=30)
        back_button.pack_forget()

    # Submit button
    def submit_user():
        nonlocal tree, scrollbar
        name = name_entry.get()

        if not name:
            messagebox.showerror("Error", "Name field is required")
            return

        try:
            users = search_user(name)  
            if not users:
                messagebox.showinfo("Not Found", "User not found.")
                return
            
            search_user_window.title(f"Search Results for '{name}'") 
            form_frame.pack_forget() 

            columns = ("User_ID", "Name", "Phone_number", "Email", "Address", "Signup_date")
            tree = ttk.Treeview(search_user_window, columns=columns, show='headings')

            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=140, anchor='center')

            for user in users:
                tree.insert("", tk.END, values=user)

            tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

            # Adding scrollbar
            scrollbar = ttk.Scrollbar(search_user_window, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscroll=scrollbar.set)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            back_button.pack(pady=10)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to find user: {e}")

    tk.Button(form_frame, text="Search", font=("Arial", 12), bg="#4CAF50", fg="white", command=submit_user).pack(pady=10)
    back_button = tk.Button(search_user_window, text="Back to Search", font=("Arial", 12), bg="#2196F3", fg="white", command=reset_to_search)


# Function to open the Delete User window

def open_delete_user():
    delete_user_window = tk.Toplevel()
    delete_user_window.title("Delete User")
    delete_user_window.geometry("400x200")
    delete_user_window.configure(bg="#E2EAF4")
    
    tk.Label(delete_user_window, text="Enter User ID", font=("Arial", 12), bg="#FBE9E7").pack(pady=20)
    user_id_entry = tk.Entry(delete_user_window, font=("Arial", 12))
    user_id_entry.pack(pady=10)

    def delete_action():
        user_id = user_id_entry.get().strip()

        if not user_id:
            messagebox.showerror("Error", "User ID is required.")
            return

        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete user ID {user_id}?")
        if not confirm:
            return

        success, message = delete_user(user_id)
        if success:
            messagebox.showinfo("Success", message)
            delete_user_window.destroy()
        else:
            messagebox.showerror("Error", message)

    tk.Button(delete_user_window, text="Delete", font=("Arial", 12), bg="#E53935", fg="white", command=delete_action).pack(pady=20)


# Function to open the Update user window

def open_update_user():
    update_user_window = tk.Toplevel()
    update_user_window.title("Update User info")
    update_user_window.geometry("400x550")
    update_user_window.configure(bg="#E2EAF4")

    # Labels and Entry Fields
    entries = {}
    fields = ["User ID", "Name", "Phone number", "Email", "Address", "Signup date"]
    
    for field in fields:
        tk.Label(update_user_window, text=field, font=("Arial", 12), bg="#E2EAF4").pack(pady=5)
        entry = tk.Entry(update_user_window, font=("Arial", 12))
        entry.pack(pady=5)
        entries[field] = entry

    # Submit button 
    def submit_update():
        values = {field: entries[field].get() for field in fields}
        
        if not all(values.values()):
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            update_user(
                values["User ID"],
                values["Name"],
                values["Phone number"],
                values["Email"],
                values["Address"],
                values["Signup date"]
            )
            messagebox.showinfo("Success", "updated successfully.")
            update_user_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update: {e}")

    tk.Button(update_user_window, text="Update", font=("Arial", 12), bg="#4CAF50", fg="white", command=submit_update).pack(pady=20)


root = tk.Tk()
root.title("Library Management System")
root.geometry("800x800")
root.config(bg="#E2EAF4")

# Title
title_label = tk.Label(
    root,
    text="Library Management System",
    font=("Cambria", 25, "bold"),
    bg="#AEAEFF",
    fg="#000000",
    padx=10,
    pady=10
)
title_label.pack(pady=30)

# Button Grid Frame
btn_frame = tk.Frame(root, bg="#E2EAF4")
btn_frame.pack(pady=20)

# Button Style
button_opts = {
    "font": ("Arial", 12),
    "bg": "#FFFFFF",
    "fg": "#000000",
    "width": 20,
    "height": 2,
    "padx": 10,
    "pady": 5
}

tk.Button(btn_frame, text="Add Book", command=open_add_book, **button_opts).grid(row=0, column=0, padx=10, pady=10)
tk.Button(btn_frame, text="Issue Book", command=open_issue_book, **button_opts).grid(row=1, column=0, padx=10, pady=10)
tk.Button(btn_frame, text="View Issued Books", command=open_view_issued_books, **button_opts).grid(row=2, column=0, padx=10, pady=10)
tk.Button(btn_frame, text="Return Book", command=open_return_book, **button_opts).grid(row=3, column=0, padx=10, pady=10)
tk.Button(btn_frame, text="View Books", command=open_view_books, **button_opts).grid(row=4, column=0, padx=10, pady=10)
tk.Button(btn_frame, text="Update Book Info", command=open_update_book, **button_opts).grid(row=5, column=0, padx=10, pady=10)
tk.Button(btn_frame, text="Search Book", command=open_search_book, **button_opts).grid(row=6, column=0, padx=10, pady=10)
tk.Button(btn_frame, text="Delete Book", command=open_delete_book, **button_opts).grid(row=7, column=0, padx=10, pady=10)

tk.Button(btn_frame, text="Add User", command=open_add_user, **button_opts).grid(row=0, column=1, padx=10, pady=10)
tk.Button(btn_frame, text="View Users", command=open_view_users, **button_opts).grid(row=1, column=1, padx=10, pady=10)
tk.Button(btn_frame, text="Search User", command=open_search_user, **button_opts).grid(row=2, column=1, padx=10, pady=10)
tk.Button(btn_frame, text="Update User Info", command=open_update_user, **button_opts).grid(row=3, column=1, padx=10, pady=10)
tk.Button(btn_frame, text="Delete User", command=open_delete_user, **button_opts).grid(row=4, column=1, padx=10, pady=10)

root.mainloop()
