# define some python functions for working with the neurotree API

try:
    import urllib2
except:
    import urllib.request as urllib2
import json
import numpy as np

def url2json(url):
    response = urllib2.urlopen(url)
    string = response.read().decode('utf-8')
    string = string.replace('""','"').replace(':",',':"",').replace('"C.Besta"','C. Besta"')
    try:
        data = None if not len(string) else json.loads(string, encoding='bytes') 
    except ValueError:
        raise Exception("%s cannot be parsed." % string)
    return data

base_api_url = 'http://neurotree.org/'
def get_neurotree_node_id_from_pmid(pmid):
    query_url = base_api_url + 'beta/include/check_pmid.php?term=%s' % pmid
    data = url2json(query_url)
    if data:
        for author in data:
#             print author['authorRank']
#             print author['label']
            if author['authorRank'] == 0 :
                node_id = author['pid']
                return node_id
        return None

def get_neurotree_node_info(neurotree_node_id):
    query_url = base_api_url + 'neurotree/jsonQuery.php?querytype=node&pid=%s' % neurotree_node_id
    data = url2json(query_url)
    info = None if data in [None,[]] else data[0]
    return info
    
def get_investigator_path_len(neurotree_node_id_1, neurotree_node_id_2):
    if neurotree_node_id_1 == neurotree_node_id_2:
        return 0, None
    if neurotree_node_id_1 is None or neurotree_node_id_2 is None:
        return None, None
    DEFAULT_MAX_STEPS = 20
    query_url = base_api_url + 'neurotree/distance.php?pid1=%s&pid2=%s&refresh=1&includera=1&includepd=1&includers=1&backonly=1&dispformat=json&maxsteps=%s' %  (neurotree_node_id_1, neurotree_node_id_2, DEFAULT_MAX_STEPS)
    data = url2json(query_url)
    print(data)
    if data:
        if data['stepstaken'] == DEFAULT_MAX_STEPS:
            path_len = np.inf
            common_inv_name = None
        elif 'stepcount' in data and data['stepcount']:
            path_len = data['stepcount']
            common_inv = data['path1'][0]
            #common_inv_name = get_neurotree_node_info(common_inv)['lastname']
            common_inv_name = common_inv
        else:
            path_len = None
            common_inv_name = None
        #print common_inv_name
    else:
        path_len = np.inf
        common_inv_name = None
        
    return path_len, common_inv_name