from py_babelnet.calls import BabelnetAPI
import ast

from utils_semanticSimilarity import *

# SENSE IDENTIFICATION utils

"""
Calculate similarity score (based on cosine similarity) of a list of couple of terms from Nasari vector.
Input:
    record: list of couples of words
    nasari: list of nasari vector
    babelSenses: list of Babel senses
Output:
    nasari_score: list of score between words in form [[word1, word2, score]]
"""
def getNasariScoreSenses(record, nasari, babelSenses):
    
    id_word, id_vect = getDictNasariBabel(nasari)
    nasari_score = []

    for rec in record:
        babel_id1 = getBabelId(babelSenses, rec[0])  # Babel id list word 1
        babel_id2 = getBabelId(babelSenses, rec[1])  # Babel id list word 2

        if len(babel_id1) > 0 and len(babel_id2) > 0:
            score = bestSenseSimilarity(babel_id1,babel_id2, id_vect) # [id_sense_word1, id_sense_word2, score]
            nasari_score.append([rec[0], rec[1], score[0], score[1], rec[2], round(score[2],2)])
            #nasari_score.append([rec[0], rec[1], score[0], score[1], score])    # [word1, word2, id_sense_word1, id_sense_word2]
        else:
            nasari_score.append([rec[0], rec[1], "_" , "_" , rec[2], 0])
    return nasari_score

"""
For each Babel sense in senses list, create a list of terms associated to it
Input:
    senses: list with form [word1, word2, id_sense_word1, id_sense_word2]
    babelInfo: list of babel senses associated to babel_id
    useAPI: Boolean value to indicate if use or not Babel API (extractBabelTermAPI() function)
Output:
    sensesTerms: list with form [word1, word2, id_sense_word1, id_sense_word2, Terms_in_BS1 Terms_in_BS2]
"""
def getBabelTerms(senses, babelInfo, useAPI):
    ss = []
    for s in senses:
        row = []
        #row1 = []
        #row2 = []

        if s[2] != "_" and s[3] != "_":
            if useAPI:
                babel_term1 = extractBabelTermAPI(s[2]) 
                babel_term2 = extractBabelTermAPI(s[3])
            else:
                babel_term1 = extractBabelTerm(s[2], babelInfo)
                babel_term2 = extractBabelTerm(s[3], babelInfo)

            #row = [s[0],s[1],s[2],s[3],s[4],s[5], list(babel_term1),list(babel_term2)]
            row = [s[0],s[1],s[2],s[3], list(babel_term1),list(babel_term2)]
            ss.append(row)
            """row1 = [s[2], list(babel_term1)]
            row2 = [s[3], list(babel_term2)]
            ss.append(row1)
            ss.append(row2)"""
    return ss

"""
Get all senses associated to 
Input:
    babel_id
    lemma: word
Output:
    terms: terms associated to babel_id
"""
def extractBabelTermAPI(babel_id):
    api = BabelnetAPI('034fb2dd-f5af-4840-aab7-917260affe5c')
    #senses = api.get_senses(lemma=lemma,  searchLang="IT")
    senses = api.get_synset(id=babel_id, targetLang="IT")

    terms = []
    for key,value in senses.items():
        if key == "senses":
            for i in value:
                terms.append(i['properties']['fullLemma'])
    return terms

"""
Extract Babel senses from babel_id (offline use of Babebl API)
Input:
    babel_id: id to search
    babelInfo: list of terms associated to babel_id
Output:
    terms: terms associated to babel_id
"""
def extractBabelTerm(babel_id, babelInfo):
    terms = []
    for el in babelInfo:
        if el[0] == babel_id:
            terms = el[1]
    return terms

"""
Save the list in form [word1, word2, id_sense_word1, id_sense_word2, Terms_in_BS1 Terms_in_BS2]
Input:
    path: path where save the list
    babel_list: list to save
"""
def saveBabelNetList(path, babel_list):
    file = open(path, 'a')
    for el in babel_list:
        file.write(str(el[0]) + "\t" + str(el[1]) + "\t" + str(el[2]) + "\t" + str(el[3]) + "\n\n")
        file.write(str(el[4]) + "\n")
        file.write(str(el[5]) + "\n\n") # Per ottenere un output più compatto rimuovere i vari "\n"
        file.write("--\n\n")
        #file.write(str(el[0]) + "\t" + str(el[1]) + "\n")
    file.close()

"""
Get a list and return another list in form [babel_id, list_of_terms]
Input:
    inputList: list to convert
"""
def getBabelInfo(inputList):
    babelInfo = []
    for line in inputList:
        r = []
        row = line.split("\t")
        r = [row[0], ast.literal_eval(row[1])]
        babelInfo.append(r)
    return babelInfo