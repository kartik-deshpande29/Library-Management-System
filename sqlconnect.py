import sqlite3
import os
from prettytable import PrettyTable

# Function to clear the screen
def clearscr():
    _ = os.system('cls')

# Function to create a connection to SQLite database
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    return conn

# Function to update records in book table
def update_table_books(conn, data):
    sql = ''' INSERT INTO book_records(name, barcode, author, price)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, data)
    conn.commit()
    print("Updated Book")

# Function to show all book records
def show_all_book_records(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM book_records")

    rows = cur.fetchall()
    print()
    print("************** Book details **************")
    print()
    t = PrettyTable(['SR', 'Name', 'Code', 'Author', 'Price'])
    for row in rows:
        t.add_row([row[0], row[1], row[2], row[3], row[4]])
    print(t)

# Function to add a new book record
def add_new_book_record(conn):
    print()
    input_name = input("Input Book name  : ")
    input_code = input("Input Book code  : ")
    input_author = input("Input Book Author: ")
    input_price = input("Input Book price : ")
    with conn:
        data = (input_name, input_code, input_author, input_price)
        update_table_books(conn, data)

# Function to search for a book record in the database
def search_book_record(conn):
    print()
    input_name = input("Input book name to search: ")
    cur = conn.cursor()
    cur.execute("SELECT * FROM book_records WHERE name LIKE ?", ('%' + input_name + '%',))
    rows = cur.fetchall()
    print()
    print("Search results....")
    print()
    t = PrettyTable(['SR', 'Name', 'Code', 'Author', 'Price'])
    for row in rows:
        t.add_row([row[0], row[1], row[2], row[3], row[4]])
    print(t)

# Function to delete a book record
def delete_book_record(conn):
    print()
    show_all_book_records(conn)
    print()
    input_rec = input("Input SR# to Delete: ")
    cur = conn.cursor()
    cur.execute("SELECT * from book_records WHERE SR=?", (input_rec,))
    row = cur.fetchone()
    print()
    data = (input_rec,)
    sql = ''' DELETE from book_records WHERE SR = ?'''
    cur.execute(sql, data)
    conn.commit()
    print()
    print("Deleted record...")
    print()
    show_all_book_records(conn)

# Function to update a book record
def update_book_record(conn):
    print()
    show_all_book_records(conn)
    print()
    input_rec = input("Input SR# to update: ")
    cur = conn.cursor()
    cur.execute("SELECT * from book_records WHERE SR=?", (input_rec,))
    row = cur.fetchone()
    print()
    input_name = input("Input new Book name [{}]  : ".format(row[1]))
    input_code = input("Input new Book code [{}]  : ".format(row[2]))
    input_author = input("Input new Book Author [{}]: ".format(row[3]))
    input_price = input("Input new Book price [{}] : ".format(row[4]))
    name = row[1]
    code = row[2]
    author = row[3]
    price = row[4]
    if input_name:
        name = input_name
    if input_code:
        code = input_code
    if input_author:
        author = input_author
    if input_price:
        price = input_price

    data = (name, code, author, price, input_rec)
    sql = ''' UPDATE book_records SET name = ?, barcode = ?, author = ?, price = ? WHERE SR = ?'''
    cur.execute(sql, data)
    conn.commit()
    print()
    print("Updated record...")
    cur.execute("SELECT * from book_records WHERE SR=?", (input_rec,))
    rows = cur.fetchall()
    t = PrettyTable(['SR', 'Name', 'Code', 'Author', 'Price'])
    for row in rows:
        t.add_row([row[0], row[1], row[2], row[3], row[4]])
    print(t)

# Function to delete all records from the book table
def delete_all_book_records(conn):
    cur = conn.cursor()
    cur.execute("DELETE FROM book_records")
    conn.commit()
    print("All records deleted.")

# Main function
def main():
    database = r"D:\Kartik-Personal\Python-SQL-project\libmgmt.db"
    conn = create_connection(database)
    input_var = '0'
    while input_var != '7':
        clearscr()
        print("*****     Welcome to Library Management System     *****")
        print()
        print("\t[1] Add new book record")
        print("\t[2] Show all book records")
        print("\t[3] Search book record")
        print("\t[4] Update book record")
        print("\t[5] Delete book record")
        print("\t[6] Delete all book records")
        print("\t[7] Exit")
        print()
        input_var = input("Input your choice:  ")

        if input_var == '1':
            add_new_book_record(conn)
            input("Press Enter to continue...")
        elif input_var == '2':
            show_all_book_records(conn)
            input("Press Enter to continue...")
        elif input_var == '3':
            search_book_record(conn)
            input("Press Enter to continue...")
        elif input_var == '4':
            update_book_record(conn)
            input("Press Enter to continue...")
        elif input_var == '5':
            delete_book_record(conn)
            input("Press Enter to continue...")
        elif input_var == '6':
            delete_all_book_records(conn)
            input("Press Enter to continue...")
        elif input_var == '7':
            print("Thank You ....")

    conn.close()

if __name__ == '__main__':
    main()
