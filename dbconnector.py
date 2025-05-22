                        # Database connection

import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="#daimari123",
        database="LBMS")



