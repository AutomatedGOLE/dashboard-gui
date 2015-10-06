from django.shortcuts import render
import db_functions as db
import json
import simplejson

def index(request):
    return render(request, 'gui/index.html')


def duplicates_remove(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if not (x in seen or seen_add(x))]


def is_reachable(nsa, cp_connectivity):
    cp_connectivity_col0 = [row[0] for row in cp_connectivity]
    cp_connectivity_col1 = [row[1] for row in cp_connectivity]

    nsa_index = cp_connectivity_col0.index(nsa)

    if int(cp_connectivity_col1[nsa_index]) == 0:
        return 1
    else:
        return 0


def graph_data(peerswith, peerswithmismatches, unknownpeers, cp_connectivity):

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
            json_data += "{\"name\":\"" + str(nsa).replace('urn:ogf:network:', '') + "\",\"group\":1}"
        elif is_reachable(nsa, cp_connectivity):
            json_data += "{\"name\":\"" + str(nsa).replace('urn:ogf:network:', '') + "\",\"group\":5}"
        else:
            json_data += "{\"name\":\"" + str(nsa).replace('urn:ogf:network:', '') + "\",\"group\":2}"

    # Add links
    for nsa1, nsa2 in peerswith:
        if "links" not in json_data:
            json_data += " ],\"links\":[ "
        else:
            json_data += ", "
        json_data += "{\"source\":" + str(nsa_list.index(nsa1)) + ",\"target\":" + str(nsa_list.index(nsa2)) + ",\"value\":3}"

    for nsa1, nsa2 in peerswithmismatches:
        json_data += ", {\"source\":" + str(nsa_list.index(nsa1)) + ",\"target\":" + str(nsa_list.index(nsa2)) + ",\"value\":4}"

    json_data += " ]}"

    return json_data


def get_isaliasdomains(isalias):
    isalias_col0 = [row[0] for row in isalias]
    return duplicates_remove(isalias_col0)


def get_isaliasvlansdomains(isaliasvlans):
    isaliasvlans_col0 = [row[0] for row in isaliasvlans]
    return duplicates_remove(isaliasvlans_col0)


def cpm(request):

    db_connection = db.database_start()
    cursor = db_connection.cursor()

    peerswith = db.get_peerswith(cursor)
    nopeers = db.get_nopeers(cursor)
    unknownpeers = db.get_unknownpeers(cursor)
    peerswithmismatches = db.get_peerswithmismatches(cursor)
    notref = db.get_notref(cursor)
    cp_connectivity = db.get_cp_connectivity(cursor)

    db.database_end(db_connection)

    context = {'graph_data': graph_data(peerswith, peerswithmismatches, unknownpeers, cp_connectivity), 'unknownpeers' : unknownpeers, 'nopeers' : nopeers, 'peerswithmismatches': peerswithmismatches, 'notref': notref, 'cp_connectivity': simplejson.dumps(cp_connectivity)}

    return render(request, 'gui/cpm.html', context)


def dpm(request):

    db_connection = db.database_start()
    cursor = db_connection.cursor()

    isalias = db.get_isalias(cursor)
    isaliasvlans = db.get_isaliasvlans(cursor)

    db.database_end(db_connection)

    context = {'isalias' : simplejson.dumps(isalias), 'isaliasvlans' : simplejson.dumps(isaliasvlans), 'isalias_domains': get_isaliasdomains(isalias), 'isaliasvlans_domains': get_isaliasvlansdomains(isaliasvlans)}

    return render(request, 'gui/dpm.html', context)