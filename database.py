#This is to connect to the database

import pymysql
from tkinter import messagebox

def connect_to_mysql():
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="Root",
            database="teacher_postal"
        )
        return conn
    except pymysql.Error as err:
        messagebox.showerror('Error', f'Error connecting to MySQL: {err}')
        return None

def setup_database():
    try:
        con = connect_to_mysql()
        cursor = con.cursor()
        
        cursor.execute('CREATE DATABASE IF NOT EXISTS teacher_postal')
        cursor.execute('USE teacher_postal')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50),
                password VARCHAR(50),
                email VARCHAR(50)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INT NOT NULL PRIMARY KEY,
                name VARCHAR(50),
                mobile VARCHAR(15),
                email VARCHAR(50),
                address VARCHAR(100),
                gender VARCHAR(10),
                dob VARCHAR(20),
                date VARCHAR(50),
                time VARCHAR(50)
            )
        ''')

        con.commit()
        cursor.close()
        return con
    except pymysql.Error as err:
        messagebox.showerror('Error', f'Database setup failed: {err}')
        return None
