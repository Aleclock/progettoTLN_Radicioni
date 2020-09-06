
import numpy as np
import math
from nltk.corpus import wordnet as wn
import collections


class Metrics:
    """
    Calculate the maximum similarity between words based on Wu-Palmer similarity metric
    Input:
        listSynsets1: list of synsets of word
        listSynsets2: list of synsets of word
    Output:
        maximum similarity

    https://docs.huihoo.com/nltk/0.9.5/api/nltk.wordnet.similarity-pysrc.html#wup_similarity
    """
    def wuPalmerMetric (self, listSynsets1, listSynsets2):
        maxSimilarity = 0
        for ss1 in listSynsets1:
            for ss2 in listSynsets2:
                lcs= getLowestCommonSubsumer(ss1,ss2) # Lowest Common Subsumer (most specific ancestor node)

                if not lcs:
                    similarity = 0
                else:
                    lcs_depth = min_depthPath(lcs,lcs)
                    ss1_depth = min_depthPath(ss1,lcs)
                    ss2_depth = min_depthPath(ss2,lcs)
                    
                    similarity = (2 * lcs_depth) / (ss1_depth + ss2_depth)
                    
                maxSimilarity = max(similarity, maxSimilarity)

        return maxSimilarity
    
    """
    Calculate the maximum similarity between words based on Shortest Path similarity metric
    Input:
        listSynsets1: list of synsets of word
        listSynsets2: list of synsets of word
    Output:
        maximum similarity
    """
    def shortestPathMetric (self, listSynsets1, listSynsets2):
        #maxDepth = maximimDepth()
        maxDepth = 20
        maxSimilarity = 0

        for ss1 in listSynsets1:
            for ss2 in listSynsets2:
                distance = shortestPath(ss1,ss2)
                #distance = ss1.shortest_path_distance(ss2)
                similarity = ((2 * maxDepth) - distance) / (2 * maxDepth) if distance is not None else 0
                maxSimilarity = max(similarity, maxSimilarity)
    
        return maxSimilarity

    """
    Calculate the maximum similarity between words based on Leacock Chodorow similarity metric
    Input:
        listSynsets1: list of synsets of word
        listSynsets2: list of synsets of word
    Output:
        maximum similarity
    """
    def leakcockChodorowMetric (self, listSynsets1,listSynsets2):
        #maxDepth = maximimDepth()
        maxDepth = 20
        maxSimilarity = 0
        for ss1 in listSynsets1:
            for ss2 in listSynsets2:
                distance = shortestPath(ss1,ss2)
                #distance = ss1.shortest_path_distance(ss2)
                if distance is not None:
                    if distance > 0:
                        similarity = - (math.log(distance/(2 * maxDepth))) / math.log(2 * maxDepth + 1)
                    else:
                        similarity = - (math.log(1/(2 * maxDepth + 1))) / math.log(2 * maxDepth + 1)
                else:
                    similarity = 0
                
                maxSimilarity = max(similarity, maxSimilarity)
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
    
    """
    NLTK Shortest Path similarity metric (as a reference)
    """
    def shortestPathMetricAPI (self, listSynsets1, listSynsets2):
        maxSimilarity = 0
        for ss1 in listSynsets1:
            for ss2 in listSynsets2:
                spSimilarity = ss1.path_similarity(ss2) or 0
                maxSimilarity = max(spSimilarity, maxSimilarity)
        return maxSimilarity

    """
    NLTK Leacock Chodorow similarity metric (as a reference)
    """
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
    commons_hypernyms: list of common synsets
"""
def getCommonSubsumer(ss1,ss2):
    h1 = ss1._all_hypernyms # all hypernym
    h2 = ss2._all_hypernyms # all hypernym
    common_hypernyms = list(h1.intersection(h2))
    return common_hypernyms


"""
Return the lowest common subsumer between two synsets.
From list of common hypernyms, the least common hypernym is that with the maximum distance from synset to root
Input:
    ss1: synset 1
    ss2: synset 2
Output:
    lowest common subsumer
"""
def getLowestCommonSubsumer (ss1, ss2):
    #commons_api = ss1.lowest_common_hypernyms(ss2)
    common_hypernyms = getCommonSubsumer(ss1,ss2)
    
    lch_index = 0   # lch depth  
    lch = None  # lowest common hypernyms

    for s in common_hypernyms:
        if max_depthPath(s) > lch_index:
            lch_index = max_depthPath(s)
            lch = s

    return lch
    

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
    paths = list(filter(lambda x: lcs in x, paths))  # Select only path containing lcs
    depth = (min(len(path) for path in paths))  # Get length of list of shortest path (minor depth)
    return depth

"""
Return the max depth from the synset to the root
"""
def max_depthPath(synset):
    paths = synset.hypernym_paths()
    depth = (max(len(path) for path in paths))    
    return depth

"""
Calculate distance between root and the element of list
Input: 
    list: list of synset
    ss1: reference synset
Ouput: 
    distance from g (element of list) and ss1
"""
def getSubDistance(list, ss1):
    for g in list:
        if (g == ss1):
            return list.index(g)


"""
Calculate the shortest path between two synsets
"""
def shortestPath(ss1, ss2):
    #pathDistanceAPI = ss1.shortest_path_distance(ss2)
    
    # VERSIONE PERSONALE (CON ERRORI)
    cs = getCommonSubsumer(ss1,ss2)

    if (len(cs) == 0):  # Non ci sono antenati antenati comuni
        return None
    
    lcs = getLowestCommonSubsumer(ss1,ss2)
    if lcs is None:
        return None

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
    
    # VERSIONE NLTK (uguale a quella implementata nella funzione NTLK shortest_path_distance() )
    """
    dist_dict1 = ss1._shortest_hypernym_paths(simulate_root=False)
    dist_dict2 = ss2._shortest_hypernym_paths(simulate_root=False)
    
    inf = float("inf")
    minDist = inf
    for synset, d1 in dist_dict1.items():
        d2 = dist_dict2.get(synset, inf)
        minDist = min(minDist, d1 + d2)"""

    return minDist

"""
Return the maximum depth of WordNet
https://stackoverflow.com/questions/36206023/wordnet-3-0-maximum-depth-of-the-taxonomy
"""
def maximimDepth():
    return max(max(len(hyp_path) for hyp_path in ss.hypernym_paths()) for ss in wn.all_synsets())