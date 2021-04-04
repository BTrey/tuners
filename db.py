#!/usr/bin/python

import mysql.connector

ttrssdb = mysql.connector.connect(
    host='localhost',
    user='dbuser',
    password='password',
    database='db_name'
)

cursor = ttrssdb.cursor()

def read_db(param):
    query_name = "SELECT r1, r2 FROM table_name"
    if DEBUG:
        print("Attempting query {}".format(query_name))
    cursor.execute(query_name)
    result_list = cursor.fetchall()
    return result_list


def main():
    for (row1, row2) in read_db():
        print("Found values of row 1 {} and row 2 {}".format(row1, row2))

if __name__ == "__main__":
    main()

