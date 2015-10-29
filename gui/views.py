from django.shortcuts import render
import db_functions as db
import simplejson


def duplicates_remove(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


def is_reachable(nsa, cp_connectivity):
    cp_connectivity_col0 = [row[0] for row in cp_connectivity]
    cp_connectivity_col1 = [row[1] for row in cp_connectivity]

    nsa_index = cp_connectivity_col0.index(nsa)

    if int(cp_connectivity_col1[nsa_index]) != 0:
        return 1
    else:
        return 0


def is_unknown(nsa, unknowntopologies):

    #DEBUG
    f = open('/tmp/debug_info', 'w')

    for topology in unknowntopologies:
        if nsa == ''.join(topology):
            return 1
    return 0

    f.close()


def cp_graph_data(peerswith, peerswithmismatches, unknownpeers, cp_connectivity):

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


def dp_graph_data(isalias, isaliasvlans, isaliasmatches, unknowntopologies):

    json_data = ''

    isaliasvlans_col0 = [row[0] for row in isaliasvlans]

    isalias_col0_new = []
    isalias_col2_new = []

    isalias_col0 = [row[0] for row in isalias]
    isalias_col2 = [row[2] for row in isalias]

    pos = 0

    for topology in isalias_col2:
        if topology != '':
            isalias_col0_new.append(isalias_col0[pos])
            isalias_col2_new.append(isalias_col2[pos])
        pos += 1

    isaliasmatches_col0 = [row[0] for row in isaliasmatches]
    isaliasmatches_col2 = [row[2] for row in isaliasmatches]

    isalias_list = duplicates_remove(isalias_col0_new + isalias_col2_new)
    isaliasmatches_list = duplicates_remove(isaliasmatches_col0 + isaliasmatches_col2)

    nsa_list = duplicates_remove(isaliasmatches_list + isalias_list)

    # Add nodes
    for nsa in nsa_list:
        if not json_data:
            json_data = "{ \"nodes\":[ "
        else:
            json_data += ", "

        if is_unknown(nsa, unknowntopologies):
            json_data += "{\"name\":\"" + str(nsa).replace('urn:ogf:network:', '') + "\",\"group\":1}"
        elif nsa in isalias_col0_new or nsa in isaliasvlans_col0:
            json_data += "{\"name\":\"" + str(nsa).replace('urn:ogf:network:', '') + "\",\"group\":2}"
        else:
            json_data += "{\"name\":\"" + str(nsa).replace('urn:ogf:network:', '') + "\",\"group\":5}"

    # Add links
    for nsa1, nsa1_port, nsa2, nsa2_port in isaliasmatches:
        if "links" not in json_data:
            json_data += " ],\"links\":[ "
        else:
            json_data += ", "
        json_data += "{\"source\":" + str(nsa_list.index(nsa1)) + ",\"target\":" + str(nsa_list.index(nsa2)) + ",\"value\":3}"

    for nsa1, nsa1_port, nsa2, nsa2_port in isalias:
        if nsa2:
            json_data += ", {\"source\":" + str(nsa_list.index(nsa1)) + ",\"target\":" + str(nsa_list.index(nsa2)) + ",\"value\":3}"

    json_data += " ]}"

    return json_data


def get_domains(array):
    col0 = [row[0] for row in array]
    return duplicates_remove(col0)


def get_cp_overview(peerswith, nopeers, unknownpeers, peerswithmismatches, notref, cp_connectivity):

    domains_list = [row[0] for row in cp_connectivity]

    # domain, #peerswith, nopeers, #unknownpeers, #peerswithmismatches, notref, cp_connectivity
    overview = []

    for domain in domains_list:
        peerswith_count = [row[0] for row in peerswith].count(domain)
        peerswithmismatches_count = [row[0] for row in peerswithmismatches].count(domain)
        unknownpeers_count = [row[0] for row in unknownpeers].count(domain)

        # It will be "has peers?" on the overview table.
        if any(domain in s for s in nopeers):
            has_nopeers = 'No'
        else:
            has_nopeers = 'Yes'

        # It will be "referenced?" on the overview table.
        if any(domain in s for s in notref):
            is_notref = 'No'
        else:
            is_notref = 'Yes'

        connectivity_index = [row[0] for row in cp_connectivity].index(domain)
        connectivity_result = [row[1] for row in cp_connectivity][connectivity_index]

        if connectivity_result > 0:
            connectivity = 'Yes'
        else:
            connectivity = 'No'

        overview.append([str(domain).replace('urn:ogf:network:', ''), peerswith_count, has_nopeers, unknownpeers_count, peerswithmismatches_count, is_notref, connectivity])

    return overview


def get_dp_overview(isalias, isaliasvlans, isaliasmatches):

    isalias_domains = get_domains(isalias)
    isaliasmatches_domains = get_domains(isaliasmatches)

    domains_list = duplicates_remove(isalias_domains + isaliasmatches_domains)

    # domain, #isalias, #isaliasvlans
    overview = []

    for domain in domains_list:
        isalias_count = [row[0] for row in isalias].count(domain)
        isaliasvlans_count = [row[0] for row in isaliasvlans].count(domain)

        overview.append([str(domain).replace('urn:ogf:network:', ''), isalias_count, isaliasvlans_count])

    return overview


def overview(request):

    db_connection = db.database_start()
    cursor = db_connection.cursor()

    peerswith = db.get_peerswith(cursor)
    nopeers = db.get_nopeers(cursor)
    unknownpeers = db.get_unknownpeers(cursor)
    peerswithmismatches = db.get_peerswithmismatches(cursor)
    notref = db.get_notref(cursor)
    cp_connectivity = db.get_cp_connectivity(cursor)
    isalias = db.get_isalias(cursor)
    isaliasvlans = db.get_isaliasvlans(cursor)
    isaliasmatches = db.get_isaliasmatches(cursor)

    db.database_end(db_connection)

    cp_overview = get_cp_overview(peerswith, nopeers, unknownpeers, peerswithmismatches, notref, cp_connectivity)
    dp_overview = get_dp_overview(isalias, isaliasvlans, isaliasmatches)

    #DEBUG
    # f = open('/tmp/debug_info', 'w')
    # simplejson.dump(cp_overview, f)
    # f.write("\n\n\n DP OVERVIEW \n\n\n")
    # simplejson.dump(dp_overview, f)
    # f.close()

    context = {'cp_overview': cp_overview, 'dp_overview': dp_overview}

    return render(request, 'gui/overview.html', context)


def cpm(request):

    db_connection = db.database_start()
    cursor = db_connection.cursor()

    peerswith = db.get_peerswith(cursor)
    nopeers = db.get_nopeers(cursor)
    unknownpeers = db.get_unknownpeers(cursor)
    peerswithmismatches = db.get_peerswithmismatches(cursor)
    notref = db.get_notref(cursor)
    cp_connectivity = db.get_cp_connectivity(cursor)
    nsastopologies = db.get_nsastopologies(cursor)
    peersroles = db.get_peersroles(cursor)

    db.database_end(db_connection)

    context = {'graph_data': cp_graph_data(peerswith, peerswithmismatches, unknownpeers, cp_connectivity), 'unknownpeers' : unknownpeers, 'nopeers' : nopeers, 'peerswithmismatches': peerswithmismatches, 'notref': notref, 'cp_connectivity': simplejson.dumps(cp_connectivity), 'nsastopologies': simplejson.dumps(nsastopologies), 'peersroles': simplejson.dumps(peersroles)}

    return render(request, 'gui/cpm.html', context)


def dpm(request):

    db_connection = db.database_start()
    cursor = db_connection.cursor()

    isalias = db.get_isalias(cursor)
    isaliasvlans = db.get_isaliasvlans(cursor)
    isaliasmatches = db.get_isaliasmatches(cursor)
    switch = db.get_switch(cursor)
    unknowntopologies = db.get_unknowntopologies(cursor)
    nsastopologies = db.get_nsastopologies(cursor)

    db.database_end(db_connection)

    context = {'graph_data': dp_graph_data(isalias, isaliasvlans, isaliasmatches, unknowntopologies), 'isalias' : simplejson.dumps(isalias), 'isaliasvlans' : simplejson.dumps(isaliasvlans), 'isalias_domains': get_domains(isalias), 'isaliasvlans_domains': get_domains(isaliasvlans), 'switch_domains': get_domains(switch), 'switches': simplejson.dumps(switch), 'nsastopologies': simplejson.dumps(nsastopologies)}

    return render(request, 'gui/dpm.html', context)