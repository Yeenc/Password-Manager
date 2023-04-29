import tkinter as tk
import mysql.connector
from cryptography.fernet import Fernet

# create the main window
window = tk.Tk()

cursor = None
conn = None

def connect():
    global cursor, conn
    try:
        conn = mysql.connector.connect(
        host='localhost',
            port=3306,
            user='root',
            password='',
            database='password_manager'
        )
        cursor = conn.cursor()
        print("Connected")
    except mysql.connector.Error as e:
        print(f"Error: {e}")

def disconnect():
    global cursor, conn
    try:
        cursor.close()
        conn.close()
        print("Disconnected")
    except mysql.connector.Error as e:
        print(f"Error: {e}")

def addTest():
    global cursor, conn
    key = Fernet.generate_key()
    fernet = Fernet(key)
    
    if conn is None:
        print("Connect to the database first!")
    else:
        inp1 = input("Type your login: ").encode()
        inp2 = input("Type your password: ").encode()
        encrypted_login = fernet.encrypt(inp1)
        encrypted_pass = fernet.encrypt(inp2)

        query = f"INSERT INTO `passes` (`Login`, `Password`) VALUES ('{encrypted_login.decode()}', '{encrypted_pass.decode()}')"
    

    try:
        cursor.execute(query)
        conn.commit()
        print("Data added")
    except mysql.connector.Error as e:
        print(f"Error: {e}")

def deleteTest():
    global cursor, conn
    query = "DELETE FROM `passes`"
    try:
        cursor.execute(query)
        conn.commit()
        print("Test data deleted")
    except mysql.connector.Error as e:
        print(f"Error: {e}")

def showAll():
    global cursor, conn
    
    try:
        key = Fernet.generate_key()
        fernet = Fernet(key)
    except KeyError as e:
        print(f"Error: {e}")

    query = "SELECT * from `passes`"
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            print(fernet.decrypt(row[0]), fernet.decrypt(row[1]), "\n")
    except mysql.connector.Error as e:
        print(f"Error: {e}")

# set the window title
window.title("Simple Passowrd Manager")

# set the window size
window.geometry("400x300")

# create a button
button1 = tk.Button(window, text="Connect to Database", command=connect)
button1.pack()
button2 = tk.Button(window,text="Disconnect from Database", command=disconnect)
button2.pack()
button3 = tk.Button(window, text="Add test Values", command=addTest)
button3.pack()
button4 = tk.Button(window, text="Delete test data", command=deleteTest)
button4.pack()
button5 = tk.Button(window, text="Show data", command=showAll)
button5.pack()

# start the GUI event loop
window.mainloop()
