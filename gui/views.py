from django.shortcuts import render
import db_functions as db

def index(request):
    return render(request, 'gui/index.html')


def cpm(request):

    db_connection = db.database_start()
    cursor = db_connection.cursor()

    #peerswith = db.get_peerswith(cursor)
    nopeers = db.get_nopeers(cursor)
    unknownpeers = db.get_unknownpeers(cursor)
    peerswithmismatches = db.get_peerswithmismatches(cursor)
    notref = db.get_notref(cursor)

    db.database_end(db_connection)

    context = {'unknownpeers' : unknownpeers, 'nopeers' : nopeers, 'peerswithmismatches': peerswithmismatches, 'notref': notref}

    return render(request, 'gui/cpm.html', context)



def dpm(request):

    db_connection = db.database_start()
    cursor =  db_connection.cursor()

    isalias = db.get_isalias(cursor)

    db.database_end(db_connection)

    context = {'isalias' : isalias}

    return render(request, 'gui/dpm.html', context)