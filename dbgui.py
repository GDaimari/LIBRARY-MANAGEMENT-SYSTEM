import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Function to connect to the database
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="your_username",
        password="your_password",
        database="your_database"
    )



