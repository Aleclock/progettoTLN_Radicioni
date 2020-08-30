import numpy as np
from numpy.linalg import norm

# SEMANTIC SIMILARITY utils

"""
Calculate similarity score (based on cosine similarity) of a list of couple of terms from Nasari vector.
Input:
    record: list of couples of words
    nasari: list of nasari vector
    babelSenses: list of Babel senses
Output:
    nasari_score: list of score between words in form [[word1, word2, score]]
"""
def getNasariScore(record, nasari, babelSenses):
    
    id_word, id_vect = getDictNasariBabel(nasari)
    nasari_score = []

    for rec in record:
        babel_id1 = getBabelId(babelSenses, rec[0])  # Babel id list word 1
        babel_id2 = getBabelId(babelSenses, rec[1])  # Babel id list word 2

        if len(babel_id1) > 0 and len(babel_id2) > 0:
            score = bestSenseSimilarity(babel_id1,babel_id2, id_vect) # [id_sense_word1, id_sense_word2, score]
            nasari_score.append([rec[0], rec[1], round(score[2],2)])
        else:
            nasari_score.append([rec[0], rec[1], 0])

    return nasari_score


"""
Calculate the best similarity value between two words babel_id's list
Input:
    babel_id1: babel_id list word 1
    babel_id2: babel_id list word 2
    id_vect: dictionary babel_id -> nasari vector
Output:
    maxSimilarity: max similarity value between two words [0: best babel_id sense word 1,1: best babel_id word 2, 2: similarity value]
"""
def bestSenseSimilarity(babel_id1,babel_id2, id_vect):
    
    nasariVector_w1 = []    # list of tuple (id, nasari_vector)
    nasariVector_w2 = []

    for id in babel_id1:
        vect = id_vect.get(id)
        if vect:
            nasariVector_w1.append((id, vect))

    for id in babel_id2:
        vect = id_vect.get(id)
        if vect:
            nasariVector_w2.append((id,vect))
    
    maxSimilarity = ["","",0]

    for vw1 in nasariVector_w1:     # for each vector_word1
        for vw2 in nasariVector_w2:
            x = vw1[1]  # Nasari vector word 1
            y = vw2[1]
            sim = cosineSimilarity(x,y)
            if sim > maxSimilarity[2]:
                maxSimilarity[0] = vw1[0]
                maxSimilarity[1] = vw2[0]
                maxSimilarity[2] = sim
            
    return maxSimilarity


"""
Calculate Cosine similarity between two vectors
Input: 
    x: Nasari vector word 1
    y: Nasari vector word 2
Output:
    sim: Cosine similarity between two vectors
"""
def cosineSimilarity(x, y):
    x = np.array(x, dtype=float)
    y = np.array(y, dtype=float)
    sim = np.inner(x, y)/(norm(x) * norm(y))
    return sim


"""
Allow to map/link Babel id to Nasari vector and word. This function return two dictionary:
    - link babel id to a word
    - link babel id to nasari vector
Input:
    nasari: nasari list
Output:
    id_word: dictionary with form   -> id_word[babel_id] = word
    id_vector: dictionary with form -> id_vector[babel_id] = vector
"""
def getDictNasariBabel(nasari):
    id_word = {}
    id_vector = {}
    for record in nasari:
        id_word[record[0]] = record[1]  # Map babel id (record[0]) to word (record[1])
        id_vector[record[0]] = record[2]  # Map babel id (record[0]) to word (record[2])
    return id_word, id_vector


"""
Extract a score list from a list in form [[word1, word2, score]]
Input:
    list: list with form [[word1, word2, score]]
Output:
    score: list with form [score1, score2, ...]
"""
def getScore(list):
    score = []
    for el in list:
        score.append(float(el[2]))
    return score


"""
Extract all babel_id associated to word
Input:
    babel: babel senses list
    word: word to search
Output:
    list of babel_id
"""
def getBabelId(babel, word):
    for s in babel:
        if word == s[0]:
            return s[1]
    return []


"""
Convert list in a Nasari list in which each element is a list with the following elements: [0: id, 1: word, 2: Nasari vector]
Input:
    list: Nasari list
Output:
    Nasari list
"""
def getNasariList(list):
    nasari = []
    for line in list:
        word = line[0].split("__")[1].lower().replace("_", " ")
        id = line[0].split("__")[0]
        vector = line[1:-1]
        nasari.append([id, word, vector])
    return nasari


"""
Convert a list in another list (Babel id list) in which each element is a list with the following elements: [0:word, 1: babel_id list]
Input:
    list
Output:
    Bebel id list
"""
def getBabelList(list):
    babel = []
    babel_el = []
    bebel_el_senses = []

    for l in list:
        if "#" in l:
            babel_el.append(bebel_el_senses)
            babel.append(babel_el)
            
            babel_el = []
            bebel_el_senses = []

            word = l.replace("#","").replace("\n","")
            babel_el.append(word)
        else:
            bebel_el_senses.append(l.replace("\n",""))
    return babel