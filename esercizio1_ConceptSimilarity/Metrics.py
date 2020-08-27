
import numpy as np
import math
from nltk.corpus import wordnet as wn
import collections

"""
Lista funzioni e correttezza

getCommonSubsumer > Dovrebbe essere corretta
getLowestCommonSubsumer > Funziona correttamente    sbaglia una volta sola per motivi strani
min_depthPath > dà risultati diversi rispetto a min_depth()
getSubDistance
shortestPath > Non funziona sempre
"""

class Metrics:

    # https://docs.huihoo.com/nltk/0.9.5/api/nltk.wordnet.synset.Synset-class.html


    # https://docs.huihoo.com/nltk/0.9.5/api/nltk.wordnet.similarity-pysrc.html#wup_similarity
    def wuPalmerMetric (self, listSynsets1, listSynsets2):
        maxSimilarity = 0
        for ss1 in listSynsets1:
            for ss2 in listSynsets2:
                lcs= getLowestCommonSubsumer(ss1,ss2) # Least Common Subsumer (most specific ancestor node)

                if not lcs:
                    similarity = 0
                else:
                    """lcs_depth = min_depthPath(lcs,lcs)
                    ss1_depth = shortestPath(ss1,lcs) + lcs_depth
                    ss2_depth = shortestPath(ss2,lcs) + lcs_depth"""

                    lcs_depth = min_depthPath(lcs,lcs)
                    ss1_depth = min_depthPath(ss1,lcs)
                    ss2_depth = min_depthPath(ss2,lcs)
                    
                    similarity = (2 * lcs_depth) / (ss1_depth + ss2_depth)
                    
                maxSimilarity = max(similarity, maxSimilarity)

        return maxSimilarity
    
    def shortestPathMetric (self, listSynsets1, listSynsets2):
        #maxDepth = maximimDepth()
        maxDepth = 20
        maxSimilarity = 0

        for ss1 in listSynsets1:
            for ss2 in listSynsets2:
                distance = shortestPath(ss1,ss2)
                #distance = ss1.shortest_path_distance(ss2)

                similarity = ((2 * maxDepth) - distance) / (2*maxDepth) if distance is not None else 0
                maxSimilarity = max(similarity, maxSimilarity)
    
        return maxSimilarity

    # TODO arrivato qui, mi sta dando problemi nel calcolo della similarità
    def leakcockChodorowMetric (self, listSynsets1,listSynsets2):
        #maxDepth = maximimDepth()
        maxDepth = 20
        maxSimilarity = 0
        for ss1 in listSynsets1:
            for ss2 in listSynsets2:
                distance = shortestPath(ss1,ss2)
                #distance = ss1.shortest_path_distance(ss2)
                similarity = - (np.log((distance or 1.)/(2*maxDepth))) / np.log((2*maxDepth) + 1) # if depth is None -> 1
                
                if distance is not None:
                    if distance > 0:
                        similarity = - (math.log(distance/(2 * maxDepth))) / math.log(2 * maxDepth + 1)
                    else:
                        similarity = - (math.log(1/(2 * maxDepth + 1))) / math.log(2 * maxDepth + 1)
                else:
                    similarity = 0
                
                maxSimilarity = max(similarity, maxSimilarity)
    
        #return maxSimilarity/(np.log((2*maxDepth)+1))
        return maxSimilarity

    """
    NLTK Wu Palmer similarity metric (as a reference)
    """
    def wuPalmerMetricAPI (self, listSynsets1, listSynsets2): 
        maxSimilarity = 0
        for ss1 in listSynsets1:
            for ss2 in listSynsets2:
                wuSimilarity = ss1.wup_similarity(ss2) or 0
                maxSimilarity = max(maxSimilarity, wuSimilarity)
        
        return maxSimilarity
    
    def shortestPathMetricAPI (self, listSynsets1, listSynsets2):
        maxSimilarity = 0
        for ss1 in listSynsets1:
            for ss2 in listSynsets2:
                spSimilarity = ss1.path_similarity(ss2) or 0
                maxSimilarity = max(spSimilarity, maxSimilarity)
        
        return maxSimilarity

    def leakcockChodorowMetricAPI (self, listSynsets1,listSynsets2):
        maxSimilarity = 0
        for ss1 in listSynsets1:
            for ss2 in listSynsets2:
                try:
                    lchSimilarity = ss1.lch_similarity(ss2)
                except:
                    lchSimilarity = 0
                
                if lchSimilarity is not None:
                    maxSimilarity = max(maxSimilarity, lchSimilarity)
        
        return maxSimilarity


"""
Calculate a list of common hypernyms between two synsets
Synset in list with low index value are the nearest to root, while hight index value referest to farest to root (nearest to ss1 synset)
Input:
    ss1: synset 1
    ss2: synset 2
Ouput:
    commons_hypernyms: list of common synsets, formed by tuple (Synset, depth from root)
"""
def getCommonSubsumer(ss1,ss2):

    ah1 = ss1._all_hypernyms # all hypernym
    ah2 = ss2._all_hypernyms # all hypernym

    comm = list(ah1.intersection(ah2))

    """
    hypernym_paths
    Get the path(s) from this synset to the root, where each path is a list of the synset nodes traversed on the way to the root.
    :return: A list of lists, where each list gives the node sequence connecting the initial ``Synset`` node and a root node.
    """
    hp1 = ss1.hypernym_paths()
    hp2 = ss2.hypernym_paths()

    commons_hypernyms = []
    commons_api = ss1.common_hypernyms(ss2)

    for h in hp1:
        for k in hp2:
            zipped = list(zip(h, k))  # unisce 2 liste in una lista di tuple

            common = None
            for i in range(len(zipped)):
                if (zipped[i][0] != zipped[i][1]):
                    break
                common = (zipped[i][0],i) # L'indice è utile per tenere conto della profondità

                if common is not None and common not in commons_hypernyms:
                    commons_hypernyms.append(common)

    #return commons_hypernyms
    return comm


"""
Return the lowest common subsumer between two synsets.
getCommonSubsumer() ritorna gli iperonimi comuni tra i due synset. L'indice corrisponde alla distanza dell'iperonimo dal root (elemento più generico).
in questo metodo prendo l'elemento meno generico in comune tra i due (il primo, quello più lontano dal root). 
Effettivamente corrisponde con la funzione implementata da nltk ma devo capire se ha senso.
Input:
    ss1: synset 1
    ss2: synset 2
Output:
    lowest common subsumer
"""
def getLowestCommonSubsumer (ss1, ss2):
    commons_api = ss1.lowest_common_hypernyms(ss2)
    common_hypernyms = getCommonSubsumer(ss1,ss2)
    
    lch = 0
    s_max = None

    for s in common_hypernyms:
        if max_depthPath(s) > lch:
            lch = max_depthPath(s)
            s_max = s
    
    """if commons_api != []:
        if (s_max == commons_api[0]):
            print ("--" + str(ss1), str(ss2))
            print (commons_api)
            print (s_max)
            print ("")"""

    """common_hypernyms.sort(key=lambda x: x[1], reverse=True) # Ordina la lista in base alla profondità del synset comune (ordine decrescente di profondità)

    if (len(common_hypernyms) == 0):
        return None

    #Nella funzione lowest_common_hypernyms di wordnet l'elemento da prendere è quello in posizione len(commons_api)
    if (common_hypernyms[0][0] != commons_api[-1]):
        print (ss1, ss2)
        print (commons_api)
        print (common_hypernyms)
        print ("")

    return common_hypernyms[0][0]"""

    return s_max
    

"""
Calculate the length path from the synset to the root. Path must contain lcs synset
Input:
    synset: synset
    lcs: least common subsumer
Ouput:
    depth: length of path
"""
def min_depthPath(synset,lcs):
    paths = synset.hypernym_paths()
    paths = list(filter(lambda x: lcs in x, paths))  # Seleziono solo i path che contengono lcs
    depth = (min(len(path) for path in paths))  # Prende la lunghezza della lista path con cardinalità minore (profondità minore)
    #depth_api = synset.min_depth()
    return depth

"""
Return the max depth from the synset to the root
"""
def max_depthPath(synset):
    paths = synset.hypernym_paths()
    depth = (max(len(path) for path in paths))    
    return depth

# Calculate distance between root and the element of list
# Ritorna la distanza tra il root ed un elemento della lista
def getSubDistance(list, ss1):
    for g in list:
        if (g == ss1):
            return list.index(g)


"""
Calculate the shortest path between two synsets
"""
def shortestPath(ss1, ss2):
    pathDistanceAPI = ss1.shortest_path_distance(ss2)
    
    # VERSIONE PERSONALE (CON ERRORI)
    cs = getCommonSubsumer(ss1,ss2)

    if (len(cs) == 0):  # Non ci sono antenati antenati comuni
        return None
    
    lcs = getLowestCommonSubsumer(ss1,ss2)
    if lcs is None:
        return None

    #cs.sort(key=lambda x: x[1], reverse=True) # Ordina la lista in base alla profondità del synset comune (ordine decrescente di profondità)
    #lcs = cs[0][0]

    path_s1 = ss1.hypernym_paths()
    path_s2 = ss2.hypernym_paths()

    # In this way path_s1 keep only that list that contain lcs
    path_s1 = list(filter(lambda x: lcs in x, path_s1))
    path_s2 = list(filter(lambda x: lcs in x, path_s2))
    
    minDist = float('inf')
    for i in path_s1:
        for k in path_s2:
            d1 = getSubDistance(i[::-1],lcs) # i[::-1] allow to reverse the list (from more specific to most generic)
            d2 = getSubDistance(k[::-1],lcs)

            if d1 is not None and d2 is not None:
                minDist = min(minDist, (d1 + d2))
    
    """if pathDistanceAPI != minDist:
        print ("cs " + str(cs))
        print ("LCS " + str(lcs))
        print (path_s1)
        print (path_s2)
        print ("")
        print (ss1._shortest_hypernym_paths(simulate_root=False))
        print (ss2._shortest_hypernym_paths(simulate_root=False))
        print ("API " + str(pathDistanceAPI), "MY " + str(minDist))
        print ("-----")"""
    
    # VERSIONE NLTK (uguale a quella implementata nella funzione shortest_path_distance() )
    """
    dist_dict1 = ss1._shortest_hypernym_paths(simulate_root=False)
    dist_dict2 = ss2._shortest_hypernym_paths(simulate_root=False)
    
    inf = float("inf")
    minDist = inf
    for synset, d1 in dist_dict1.items():
        d2 = dist_dict2.get(synset, inf)
        minDist = min(minDist, d1 + d2)"""
    
    """if pathDistanceAPI != minDist:    
        print ("-- Synsets " + str(ss1) + " , " + str(ss2))
        print ("** HCS " + str(lcs))
        print ("== common sub " + str(cs))
        print ([p[::-1] for p in path_s1])
        print ([p[::-1] for p in path_s2])
        print ("")
        print ("+++ dist (API, my) " + str(pathDistanceAPI) + " , " + str(minDist))
        print ("\n")"""

    return minDist

"""
Return the maximum depth of WordNet
"""
def maximimDepth():
    return max(max(len(hyp_path) for hyp_path in ss.hypernym_paths()) for ss in wn.all_synsets())