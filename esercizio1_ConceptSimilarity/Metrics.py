
import numpy as np
from nltk.corpus import wordnet as wn

class Metrics:

    # https://docs.huihoo.com/nltk/0.9.5/api/nltk.wordnet.synset.Synset-class.html


    # https://docs.huihoo.com/nltk/0.9.5/api/nltk.wordnet.similarity-pysrc.html#wup_similarity
    def wuPalmerMetric (self, listSynsets1, listSynsets2):
        maxSimilarity = 0
        maxSimilarityAPI = 0
        for ss1 in listSynsets1:
            for ss2 in listSynsets2:
                wuSimilarity = ss1.wup_similarity(ss2) or 0
                lcs= getLowestCommonSubsumer(ss1,ss2) 

                if not lcs:
                    similarity = 0
                else:
                    lcs_depth = depthPath(lcs, lcs)
                    ss1_depth = depthPath(ss1, lcs)
                    ss2_depth = depthPath(ss2, lcs)
                    
                    similarity = (2 * lcs_depth) / (ss1_depth + ss2_depth)
                    
                maxSimilarity = max(similarity, maxSimilarity)
                maxSimilarityAPI = max(maxSimilarityAPI, wuSimilarity)
        return maxSimilarity
    
    def shortestPathMetric (self, listSynsets1, listSynsets2):
        maxDepth = 20
        maxSimilarity = 0

        for ss1 in listSynsets1:
            for ss2 in listSynsets2:
                #spSimilarity = ss1.path_similarity(ss2)
                depth = shortestPath(ss1,ss2)
                if not depth:
                    similarity = 0
                else: 
                    similarity = 2*maxDepth - depth 
                maxSimilarity = max(similarity, maxSimilarity)
        return maxSimilarity/(2*maxDepth)

    def leakcockChodorowMetric (self, listSynsets1,listSynsets2):
        maxDepth = 20
        maxSimilarity = 0
        for ss1 in listSynsets1:
            for ss2 in listSynsets2:
                depth = shortestPath(ss1,ss2)
                similarity = -np.log((depth or 1.)/(2*maxDepth))
                maxSimilarity = max(similarity, maxSimilarity)
        return maxSimilarity/(np.log((2*maxDepth)+1))
 
def getCommonSubsumer(ss1,ss2):
    #lcs_list = ss1.lowest_common_hypernyms(ss2) # Ritorna la lista degli antenati comuni dei due synset

    """if ss1 == ss2:
        return ss1"""

    # Hypernym path of synset
    hp1 = ss1.hypernym_paths() # Return a list of length 1, so i take the first element (the entire list)
    hp2 = ss2.hypernym_paths()

    commons_hypernyms = []
    commons_api = ss1.lowest_common_hypernyms(ss2)

    for h in hp1:
        for k in hp2:
            zipped = list(zip(h, k))  # unisce 2 liste in una lista di tuple
            common = None
            for i in range(len(zipped)):
                if (zipped[i][0] != zipped[i][1]):
                    break
                common = (zipped[i][0],i)   # L'indice è utile per tenere conto della profondità
            
            if common is not None and common not in commons_hypernyms:
                commons_hypernyms.append(common)

    return commons_hypernyms

def getLowestCommonSubsumer (ss1, ss2):
    #commons_api = ss1.lowest_common_hypernyms(ss2)
    common_hypernyms = getCommonSubsumer(ss1,ss2)
    common_hypernyms.sort(key=lambda x: x[1], reverse=True) # Ordina la lista in base alla profondità del synset comune

    if (len(common_hypernyms) == 0):
        return None
    
    """#Nella funzione lowest_common_hypernyms di wordnet l'elemento da prendere è quello in posizione len(commons_api)
    if (common_hypernyms[0][0] != commons_api[-1]):
        print (commons_api)
        print (common_hypernyms)
        print ("------------------------")"""

    return common_hypernyms[0][0]
    

def depthPath(synset, lcs):
    paths = synset.hypernym_paths()

    #paths = list(filter(lambda x: lcs in x, paths))  # Seleziono solo i path che contengono lcs
    depth = (min(len(path) for path in paths)) - 1  # Prende la lunghezza della lista path con cardinalità minore (profondità minore)
    #depth_api = synset.min_depth()
    
    return depth

# Ritorna la distanza tra il root ed un elemento della lista
def getSubDistance(list, ss1):
    for g in list:
        if (g == ss1):
            """l1 = list.index(g)
            print (l1)
            break"""
            return list.index(g)

def shortestPath(ss1, ss2):
    pathDistanceAPI = ss1.shortest_path_distance(ss2)
    
    cs = getCommonSubsumer(ss1,ss2)
    if (len(cs) == 0):  # Non ci sono antenati antenati comuni
        return None
    hcs = cs[-1][0] # Highest common subsumer, Prendo l'ultimo in quanto quello più vicino ai due synset

    path_s1 = ss1.hypernym_paths()
    path_s2 = ss2.hypernym_paths()
    path_s1 = list(filter(lambda x: hcs in x, path_s1))
    path_s2 = list(filter(lambda x: hcs in x, path_s2))

    minDist = float('inf')
    """minPath1 = []
    minPath2 = []"""
    for i in path_s1:
        for k in path_s2:
            d1 = getSubDistance(i[::-1],hcs)
            d2 = getSubDistance(k[::-1],hcs)
            """if d1 < minDist1:
                print (d1)
                minPath1 = i
            if d2 < minDist2:
                print (d2)
                minPath2 = k"""
            minDist = min(minDist, (d1+d2))
    return minDist

def maximimDepth():
    return max(max(len(hyp_path) for hyp_path in ss.hypernym_paths()) for ss in wn.all_synsets())