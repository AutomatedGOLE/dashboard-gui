from django.shortcuts import render
import db_functions as db
import json

def index(request):
    return render(request, 'gui/index.html')


def duplicates_remove(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if not (x in seen or seen_add(x))]


def graph_data(peerswith, peerswithmismatches, unknownpeers):

    json_data = ''

    peerswith_col0 = [row[0] for row in peerswith]
    peerswith_col1 = [row[1] for row in peerswith]

    peerswithmismatches_col0 = [row[0] for row in peerswithmismatches]
    peerswithmismatches_col1 = [row[1] for row in peerswithmismatches]

    nsa_list = duplicates_remove(peerswith_col0 + peerswith_col1 + peerswithmismatches_col0 + peerswithmismatches_col1)

    # Add nodes
    for nsa in nsa_list:
        if not json_data:
            json_data = "{ \"nodes\":[ "
        else:
            json_data += ", "

        if nsa in [row[1] for row in unknownpeers]:
            json_data += "{\"name\":\"" + str(nsa).replace('urn:ogf:network:','') + "\",\"group\":1}"
        else:
            json_data += "{\"name\":\"" + str(nsa).replace('urn:ogf:network:','') + "\",\"group\":0}"

    # Add links
    for nsa1, nsa2 in peerswith:
        if "links" not in json_data:
            json_data += " ],\"links\":[ "
        else:
            json_data += ", "
        json_data += "{\"source\":" + str(nsa_list.index(nsa1)) + ",\"target\":" + str(nsa_list.index(nsa2)) + ",\"value\":2}"

    for nsa1, nsa2 in peerswithmismatches:
        json_data += ", {\"source\":" + str(nsa_list.index(nsa1)) + ",\"target\":" + str(nsa_list.index(nsa2)) + ",\"value\":3}"

    json_data += " ]}"


    #DEBUG
    f = open('/tmp/dashboardlog', 'w')
    f.write(json_data)
    f.close()

    return json_data


def cpm(request):

    db_connection = db.database_start()
    cursor = db_connection.cursor()

    peerswith = db.get_peerswith(cursor)
    nopeers = db.get_nopeers(cursor)
    unknownpeers = db.get_unknownpeers(cursor)
    peerswithmismatches = db.get_peerswithmismatches(cursor)
    notref = db.get_notref(cursor)

    db.database_end(db_connection)

    context = {'graph_data': graph_data(peerswith, peerswithmismatches, unknownpeers), 'unknownpeers' : unknownpeers, 'nopeers' : nopeers, 'peerswithmismatches': peerswithmismatches, 'notref': notref}

    return render(request, 'gui/cpm.html', context)


def dpm(request):

    db_connection = db.database_start()
    cursor =  db_connection.cursor()

    isalias = db.get_isalias(cursor)

    db.database_end(db_connection)

    context = {'isalias' : isalias}

    return render(request, 'gui/dpm.html', context)