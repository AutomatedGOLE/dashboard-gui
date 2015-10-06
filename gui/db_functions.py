import mysql.connector as db
from collections import defaultdict


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


def get_notref(cursor):
    query = "SELECT * FROM notref"
    cursor.execute(query)
    return cursor.fetchall()


def get_isalias(cursor):
    query = "SELECT * FROM isalias"
    cursor.execute(query)
    return cursor.fetchall()


def get_isaliasvlans(cursor):
    query = "SELECT * FROM isaliasvlans"
    cursor.execute(query)
    return cursor.fetchall()


def get_cp_connectivity(cursor):
    query = "SELECT * FROM cp_connectivity"
    cursor.execute(query)
    return cursor.fetchall()

#
# def matrix_to_dic(matrix):
#     dic = defaultdict(int)
#     for a, b in matrix:
#         dic[a] = b
#     return dic
