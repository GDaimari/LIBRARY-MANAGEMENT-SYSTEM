                        # Functions related to the tables

from dbconnector import connect_db
import datetime
from tkinter import messagebox

                        # Functions related to books table

def add_book(book_id, title, author, genre, publish_year, copies_available):
    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute( "INSERT INTO BOOKS (Book_ID, Title, Author, Genre, Publish_year, Copies_available) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (book_id, title, author, genre, publish_year, copies_available))
        db.commit()
        
    except Exception as e:
        raise e
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()
        

def search_book(title):
    try:
        db=connect_db()
        cursor=db.cursor()
        cursor.execute("SELECT * FROM BOOKS WHERE Title = %s", (title,))
        result = cursor.fetchall()
        return result
    except Exception as e:
        raise e
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()
        


def delete_book(book_id):
    try:
        db=connect_db()
        cursor=db.cursor()
        cursor.execute("SELECT * FROM BOOKS WHERE Book_ID = %s", (book_id,))
        book = cursor.fetchone()
        if not book:
            return False, "Book ID not found."
        cursor.execute("DELETE FROM BOOKS WHERE Book_ID = %s", (book_id,))
        db.commit()
        return True, "Book deleted successfully."

    except Exception as e:
        return False, f"Error occurred: {e}"

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()


def update_book(Book_id, Title, Author, Genre, Publish_year, Copies_available):
    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("UPDATE BOOKS SET Book_ID =%s, Title=%s, Author=%s, Genre=%s, Publish_year=%s, Copies_available=%s WHERE Book_ID=%s",(Book_id, Title, Author, Genre, int(Publish_year), int(Copies_available), Book_id))
        db.commit()
        db.close()
    except Exception as e:
        raise e
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()


                        # Functions related to user table

def add_user(User_id, Name, Phone_number, Email, Address, Signup_date):
    try:
        Signup_date = datetime.datetime.strptime(Signup_date, "%Y-%m-%d").date()
        db=connect_db()
        cursor=db.cursor()
        cursor.execute("INSERT INTO LIBRARY_USERS (User_ID, Name, Phone_number, Email, Address, Signup_date)"" VALUES(%s,%s,%s,%s,%s,%s)", (User_id, Name, Phone_number, Email, Address, Signup_date))
        db.commit()
    except Exception as e:
        raise e 
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()


def search_user(name):
    try:
        db=connect_db()
        cursor=db.cursor()
        cursor.execute("SELECT * FROM LIBRARY_USERS WHERE Name = %s", (name,))
        result = cursor.fetchall()
        return result
    except Exception as e:
        raise e
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()
       

def delete_user(user_id):
    try:
        db=connect_db()
        cursor=db.cursor()
        cursor.execute("SELECT * FROM LIBRARY_USERS WHERE User_ID = %s", (user_id,))
        result = cursor.fetchone()
        if not result:
            return False, "User ID not found."
        cursor.execute("DELETE FROM LIBRARY_USERS WHERE User_ID = %s", (user_id,))
        db.commit()
        return True, "User deleted successfully."

    except Exception as e:
        return False, f"Error occurred: {e}"
    except Exception as e:
        raise e
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()


def update_user(User_ID, Name, Phone_number, Email, Address, Signup_date):
    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("UPDATE LIBRARY_USERS SET User_ID = %s, Name = %s, Phone_number = %s, Email = %s, Address = %s, Signup_date = %s WHERE User_ID = %s",(User_ID, Name, Phone_number, Email, Address, Signup_date, User_ID))
        db.commit()
        db.close()
    except Exception as e:
        raise e
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()



                        # Functions related to issue table

def issue_book(Issue_id, User_id, Book_id, Issue_date, Due_date):

    try:
        Issue_date = datetime.datetime.strptime(Issue_date, "%Y-%m-%d").date()
        Due_date = datetime.datetime.strptime(Due_date, "%Y-%m-%d").date()

        db = connect_db()
        cursor = db.cursor()

        cursor.execute("SELECT Copies_available FROM BOOKS WHERE Book_ID = %s", (Book_id,))
        result = cursor.fetchone()

        if not result:
            messagebox.showerror("Error", "Book not found.")
            return

        Copies_available = result[0]
        if Copies_available <= 0:
            messagebox.showwarning("Unavailable", "No copies available for this book.")
            return

        cursor.execute(
            "INSERT INTO ISSUES (Issue_ID, User_ID, Book_ID, Issue_date, Due_date)"" VALUES (%s, %s, %s, %s, %s)",
            (Issue_id, User_id, Book_id, Issue_date, Due_date)
        )

        cursor.execute(
            "UPDATE BOOKS SET Copies_available = Copies_available - 1 WHERE Book_ID = %s",
            (Book_id,)
        )

        db.commit()
    
    except Exception as e:
        raise e 
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()


                        # Function related to return table

def book_return(User_id, Book_id, Return_date):
    try:
        db = connect_db()
        cursor = db.cursor()

        cursor.execute("""
            SELECT Issue_ID, Issue_date, Due_date
            FROM ISSUES
            WHERE Book_ID = %s AND User_ID = %s AND Status = 'Issued'
            ORDER BY Issue_date DESC LIMIT 1
        """, (Book_id, User_id))
        issue_record = cursor.fetchone()

        if not issue_record:
            messagebox.showerror("Error", "No active issue found for this book and user.")
            return

        Issue_id, Issue_date, Due_date = issue_record

        Return_date = datetime.datetime.strptime(Return_date, "%Y-%m-%d").date()

        fine = 0.0
        if Return_date > Due_date:
            days_late = (Return_date - Due_date).days
            fine = days_late * 2.0

        cursor.execute("""
            INSERT INTO RETURN_INFO (Issue_ID, User_ID, Book_ID, Return_date, Fine, Issue_date, Status)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (Issue_id, User_id, Book_id, Return_date, fine, Issue_date, 'Returned'))

        cursor.execute("""
            UPDATE BOOKS
            SET Copies_available = Copies_available + 1
            WHERE Book_ID = %s
        """, (Book_id,))

        cursor.execute("""
            UPDATE ISSUES
            SET Status = 'Returned'
            WHERE Issue_ID = %s
        """, (Issue_id,))

        db.commit()
        messagebox.showinfo("Success", f"Book returned successfully. Fine: Rs. {fine:.2f}")

    except Exception as e:
        db.rollback()
        messagebox.showerror("Error", f"Failed to return book: {e}")
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()


                           # Fetching functions

def fetch_all_books():
    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM BOOKS")
        books = cursor.fetchall()
        return books
    except Exception as e:
        raise e
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()


# functions.py

def fetch_all_issued_books():
    try:
        db=connect_db()
        cursor = db.cursor()
        query = """
            SELECT i.Issue_ID, i.User_ID, i.Book_ID, b.Title, i.Issue_date, i.Due_date
            FROM ISSUES i
            JOIN BOOKS b ON i.Book_ID = b.Book_ID
        """
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    except Exception as e:
        raise e
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()



def fetch_all_users():
    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM LIBRARY_USERS")
        users = cursor.fetchall()
        return users
    except Exception as e:
        raise e
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()







