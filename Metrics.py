
import numpy as np
from nltk.corpus import wordnet as wn

class Metrics:

    # https://docs.huihoo.com/nltk/0.9.5/api/nltk.wordnet.synset.Synset-class.html


    def wuPalmerMetric (self, listSynsets1, listSynsets2):
        maxSimilarity = 0
        #maxSimilarityWN = 0 # Similarità massima in base alla funzione WordNet wup_similarity
        for ss1 in listSynsets1:
            for ss2 in listSynsets2:
                lcs = getLowestCommonSubsumer(ss1,ss2) 

                if not lcs:
                    similarity = 0
                else:
                    """ METODO 1, non l'ho capito
                    lcs_depth = lcs.min_depth() + 1 
                    ss1_depth = ss1.shortest_path_distance(lcs) + lcs_depth
                    ss2_depth = ss2.shortest_path_distance(lcs) + lcs_depth"""

                    lcs_depth = depthPath(lcs, lcs)
                    ss1_depth = depthPath(ss1, lcs)
                    ss2_depth = depthPath(ss2, lcs)
                    
                    similarity = (2 * lcs_depth) / (ss1_depth + ss2_depth)
                    #wuSimilarity = ss1.wup_similarity(ss2)

                maxSimilarity = max(similarity, maxSimilarity)
                #maxSimilarityWN = max(wuSimilarity, maxSimilarityWN)
        #print (str(maxSimilarity) + " ---- " + str(maxSimilarityWN))
        return maxSimilarity
    
    def shortestPathMetric (self, listSynsets1, listSynsets2):
        maxDepth = 20
        #depth_max = depthMax()
        maxSimilarity = 0
        for ss1 in listSynsets1:
            for ss2 in listSynsets2:
                depth = shortestPath(ss1,ss2)
                similarity = 2*maxDepth - depth
                #spSimilarity = ss1.path_similarity(ss2)
                maxSimilarity = max(similarity, maxSimilarity)
        return maxSimilarity/(2*maxDepth)

    def leakcockChodorowMetric (self, listSynsets1,listSynsets2):
        maxDepth = 20
        #depth_max = depthMax()
        maxSimilarity = 0
        for ss1 in listSynsets1:
            for ss2 in listSynsets2:
                depth = shortestPath(ss1,ss2)
                #similarity = - log(depth/(2*maxDepth))
                similarity = -np.log((depth or 1.)/(2*maxDepth))
                maxSimilarity = max(similarity, maxSimilarity)
        return maxSimilarity/(np.log((2*maxDepth)+1))

    

def getLowestCommonSubsumer (ss1, ss2):
    lcs_list = ss1.lowest_common_hypernyms(ss2) # Ritorna la lista degli antenati comuni dei due synset
    if (len(lcs_list) == 0):
        return None
    lcs = sorted(lcs_list, key=lambda hp: hp.max_depth(), reverse=True) # Ordina gli iperonimi comuni in base alla prondità
    return lcs[0]

def depthPath(synset, lcs):
    paths = synset.hypernym_paths()
    paths = list(filter(lambda x: lcs in x, paths))  # path che contengono lcs
    return min(len(path) for path in paths)

def shortestPath(synset1, synset2):
    """lcs_list = synset1.lowest_common_hypernyms(synset2)
    path_s1 = synset1.hypernym_paths()
    path_s2 = synset2.hypernym_paths()"""

    pathDistance = synset1.shortest_path_distance(synset2)
    if pathDistance is None:
        return 0

    return pathDistance

def depthMax():
    return max(max(len(hyp_path) for hyp_path in ss.hypernym_paths()) for ss in wn.all_synsets())