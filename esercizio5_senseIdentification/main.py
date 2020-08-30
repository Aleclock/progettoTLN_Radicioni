import csv
from numpy.linalg import norm

from semeval_mapper import *
from utils_semanticSimilarity import *
from Correlation import *

# cd /Users/aleclock/Desktop/uni/TLN/radicioni/progettoTLN_Radicioni/esercizio5_senseIdentification

def saveList(path, list):
    with open(path, 'wt') as out_file:
        tsv_writer = csv.writer(out_file, delimiter='\t')
        #tsv_writer = csv.writer(out_file, delimiter='|')
        for l in list:
            tsv_writer.writerow(l)

def readFile_txt(path):
    file = open(path,"r",encoding="utf-8")
    return file.readlines()

def readFile_tsv(path):
    array = []
    with open(path, "r") as tsv:
        for line in tsv:
            row = line.split("\t")
            row[2] = row[2].replace("\n","")
            #array.append(line.split("\t"))
            array.append(row)
            #word = l.replace("#","").replace("\n","")
    return array

"""
Normalize all elements in a list    norm_el = el / max(list)
Input:
    list: list to normalize
Output:
    score_normalize: normalized list
"""
def normalizeList(list):
    max_score = max(list)
    score_normalize = [w/max_score for w in list]
    return score_normalize


def main():
    
    """ SEMANTIC SIMILARITY """

    # ---------------------------------------------
    # ----      0. INDIVIDUAZIONE COPPIE
    # Le 50 coppie (sul totale di 500 coppie presenti nel file) sono da individuare sulla base del cognome, 
    # tramite la funzione definita nel notebook semeval_mapper.ipynb.
    # ---------------------------------------------

    coupleList = getList("Clocchiatti", "./asset/it.test.data.txt") # Couple list
    #saveList("./asset/it.test.dataClocchiatti.tsv", coupleList)

    # ---------------------------------------------
    # ----      1. VALUTAZIONE DELL'ANNOTAZIONE
    #   a. La valutazione dei punteggi annotati dovrà essere condotta in rapporto alla similarità ottenuta utilizzando i vettori NASARI (versione embedded; 
    #       file mini_NASARI.tsv, nel materiale della lezione).
    #   b. La valutazione della nostra annotazione è condotta calcolando i coefficienti di Pearsons e Separman fra (la media dei) 
    #       i punteggi annotati a mano e quelli calcolati con la versione embedded di NASARI.
    # ---------------------------------------------

    clocchiatti_score = readFile_tsv("./asset/it.test.dataClocchiatti.tsv")
    mini_nasari = getNasariList(readFile_tsv("./asset/mini_NASARI.tsv"))
    babelSenses = getBabelList(readFile_txt("./asset/SemEval17_IT_senses2synsets.txt"))
    
    nasari_score = getNasariScore(clocchiatti_score, mini_nasari, babelSenses)
    
    clocchiatti_score_norm = normalizeList(getScore(clocchiatti_score))
    nasari_score_norm = normalizeList(getScore(nasari_score))

    for i, el in enumerate(clocchiatti_score):
        print (str(el[0]) + " | " + str(el[1]) + " | " + str(clocchiatti_score_norm[i]) + " | " + str(nasari_score_norm[i]))
        #print("{}% {}".format(ratio * 100, color))


    """for el, value in clocchiatti_score.items():
        print (el, value)
        #print (el[0], el[1])"""

    corr_pearson = pearson_index(clocchiatti_score_norm, nasari_score_norm)
    corr_spearman = spearman_index(clocchiatti_score_norm, nasari_score_norm)

    print (corr_pearson, corr_spearman)

    corr_pearson = pearson_index(getScore(clocchiatti_score), getScore(nasari_score))
    corr_spearman = spearman_index(getScore(clocchiatti_score), getScore(nasari_score))
    
    print (corr_pearson, corr_spearman)


    """ SENSE IDENTIFICATION """
    

main()