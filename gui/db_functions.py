import mysql.connector as db


def database_start():
    db_connection = db.connect(user='monitor', password='monitor_pass', database='dashboard')
    return db_connection


def database_end(db_connection):
    db_connection.commit()
    db_connection.close()


def get_peerswith(cursor):
    query = "SELECT * FROM peerswith"
    cursor.execute(query)
    return cursor.fetchall()


def get_nopeers(cursor):
    query = "SELECT * FROM nopeers"
    cursor.execute(query)
    return cursor.fetchall()


def get_unknownpeers(cursor):
    query = "SELECT * FROM unknownpeers"
    cursor.execute(query)
    return cursor.fetchall()


def get_peerswithmismatches(cursor):
    query = "SELECT * FROM peerswithmismatches"
    cursor.execute(query)
    return cursor.fetchall()


def get_isalias(cursor):
    query = "SELECT * FROM isalias"
    cursor.execute(query)
    return cursor.fetchall()
