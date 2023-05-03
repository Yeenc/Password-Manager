# Biblioteki
import tkinter as tk
import mysql.connector
from cryptography.fernet import Fernet
import os

# OKNO------------------------------------------------------------------------------
# Deklaracja głównego okna
window = tk.Tk()

# Tytuł okna
window.title("Simple Passowrd Manager")

# Rozmiar Okna
window.geometry("400x300")
# ----------------------------------------------------------------------------------


# KLUCZ-------------------------------------------------------------------------------
# Wygenerowanie kodu do zaszyfrowania, tworzenie nowej sesji z tym kluczem
key = Fernet.generate_key()
fernet = Fernet(key)

# Musiałem zmienić strukturę tabel w MySQL aby móc odszyfrować dane
# ALTER TABLE passes MODIFY Login BLOB;
# ALTER TABLE passes MODIFY Password BLOB;
# Typ BLOB nie dodaje żadnych znaczników do danych w przeciwieństwie do VARBINARY...
# -----------------------------------------------------------------------------------


# POŁĄCZENIE---------------------------------------------------------------------------
# Deklaracja połączenia do bazy danych, i kursora do zapytań dla bazy
cursor = None
conn = None
# ---------------------------------------------------------------------------------------


# FUNKCJE -------------------------------------------------------------------------------
# Połączenie do bazy
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

# Rozłączenie z bazą
def disconnect():
    global cursor, conn
    try:
        cursor.close()
        conn.close()
        print("Disconnected")
    except mysql.connector.Error as e:
        print(f"Error: {e}")

# Dodawanie danych do bazy
def addTest():
    global cursor, conn
    
    if conn is None:
        print("Connect to the database first!")
    else:
        inp1 = input("Type your login: ")
        inp2 = input("Type your password: ")

        inp1 = inp1.encode()
        inp2 = inp2.encode()
        
        encrypted_login = fernet.encrypt(inp1)
        encrypted_pass = fernet.encrypt(inp2)

        query = "INSERT INTO `passes` (`Login`, `Password`) VALUES (%s, %s)"
        values = (encrypted_login, encrypted_pass)

        try:
            cursor.execute(query, values)
            conn.commit()
            print("Data added")
        except mysql.connector.Error as e:
            print(f"Error: {e}")


# Usuwanie wszystkich danych z bazy
def deleteTest():
    global cursor, conn
    query = "DELETE FROM `passes`"
    try:
        cursor.execute(query)
        conn.commit()
        print("Test data deleted")
    except mysql.connector.Error as e:
        print(f"Error: {e}")

# Wyświetlanie wszystkich danych w bazie
def showAll():
    global cursor, conn

    query = "SELECT * from `passes`"
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            decrypted_login = fernet.decrypt(row[0]).decode()
            decrypted_pass = fernet.decrypt(row[1]).decode()
            print(decrypted_login, decrypted_pass, "\n")
    except mysql.connector.Error as e:
        print(f"Error: {e}")

# ---------------------------------------------------------------------------------


# Przyciski, muszą być pod funkcjami-----------------------------------------------------
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
# -------------------------------------------------------------------------------------------

# Uruchomienie okna
window.mainloop()