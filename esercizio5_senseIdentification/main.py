import csv
from numpy.linalg import norm
import os
from sklearn.metrics import cohen_kappa_score


from semeval_mapper import *
from utils_semanticSimilarity import *
from utils_senseIdentification import *
from Correlation import *

# cd /Users/aleclock/Desktop/uni/TLN/radicioni/progettoTLN_Radicioni/esercizio5_senseIdentification


"""
Save a list in .tsv format 
Input:
    path: file path
    list: list to save
"""
def saveList(path, list):
    with open(path, 'wt') as out_file:
        tsv_writer = csv.writer(out_file, delimiter='\t')
        #tsv_writer = csv.writer(out_file, delimiter='|')
        for l in list:
            tsv_writer.writerow(l)

"""
Delete file in path
Input: 
    path: path of file
"""
def clear_file(path):
    os.remove(path)


"""
Save the annotation in form:    type, frame_name, element, synset
Input:
    path: path of file
    list: list
"""
def saveList_txt (path, list):
    file = open(path, 'a')
    #file.write(el + ", " + fn.frame(frame).name + ", " + str(synset) +"\n")
    for i in list:
        #file.write(i[0] + ", " + i[1] + ", " + i[2] + ", " + str(i[3]) + "\n")
        file.write(str(i[0]) + "\t" + str(i[1]) + "\t" + str(i[2]) + "\n")
    file.close()

"""
Read a .txt file
Input:
    path: file path
Output:
    list of file lines
"""
def readFile_txt(path):
    file = open(path,"r",encoding="utf-8")
    return file.readlines()

"""
Read a .tsv file
Input:
    path: path file
Output:
    array: list of lists (each list in list is a row in file)
"""
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
Normalize all elements in a list  ->  norm_el = el / max(list)
Input:
    list: list to normalize
Output:
    score_normalize: normalized list
"""
def normalizeList(list):
    max_score = max(list)
    score_normalize = [w/max_score for w in list]
    return score_normalize

def convert_to_int(float_list):
    list = [int(x) for x in float_list]
    return list


def main():
    
    """ ---------------------
        SEMANTIC SIMILARITY 
        --------------------- """

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

    print ("\n__ Prima consegna - Semantic similarity \n")

    clocchiatti_score = readFile_tsv("./asset/it.test.dataClocchiatti.tsv")
    mini_nasari = getNasariList(readFile_tsv("./asset/mini_NASARI.tsv"))
    babelSenses = getBabelList(readFile_txt("./asset/SemEval17_IT_senses2synsets.txt"))
    
    nasari_score = getNasariScore(clocchiatti_score, mini_nasari, babelSenses)

    clear_file ("./output/nasari_score.txt")
    saveList_txt("./output/nasari_score.txt", nasari_score)
    
    clocchiatti_score_norm = normalizeList(getScore(clocchiatti_score))
    nasari_score_norm = normalizeList(getScore(nasari_score))

    corr_pearson = pearson_index(clocchiatti_score_norm, nasari_score_norm)
    corr_spearman = spearman_index(clocchiatti_score_norm, nasari_score_norm)
    

    print ("Pearson index correlation: " + str(corr_pearson))
    print ("Spearman index correlation: " + str(corr_spearman))


    """ ---------------------
        SENSE IDENTIFICATION 
        --------------------- """
    
    # ---------------------------------------------
    # ----      2a. INDIVIDUAZIONE DEI SENSI ALLA BASE DEL GIUDIZIO
    #      Il secondo compito consiste nell’individuare i sensi selezionati nel giudizio di similarità.
    #       - La domanda che ci poniamo è la seguente: quali sensi abbiamo effettivamente utilizzato quando abbiamo assegnato 
    #           un valore di similarità a una coppia di termini (per esempio, società e cultura)?
    #       - NB: questa annotazione, sebbene svolta successivamente a quella della prima consegna, deve essere coerente con l’annotazione 
    #           dei punteggi di similarità.
    #      Per risolvere questo compito partiamo dall’assunzione che i due termini funzionino come contesto di disambiguazione l’uno per l’altro.
    #      L’output di questa parte dell’esercitazione consiste in 2 Babel synset ID e dai termini del synset
    #       - il formato di output è quindi costituito da 6 campi (separatore fra campi ;a tabulazione, mentre usiamo la virgola ‘,’ come separatore all’interno   dello stesso campo):
    #           #Term1 Term2 BS1 BS2 Terms_in_BS1 Terms_in_BS2
    #           macchina bicicletta bn:00007309n bn:00010248n
    #           auto,automobile,macchina bicicletta,bici,bike
    # ---------------------------------------------

    print ("\n__ Seconda consegna - Sense identification \n")

    senses = getNasariScoreSenses(clocchiatti_score, mini_nasari, babelSenses)
    babelInfo = getBabelInfo(readFile_txt("./asset/babelInfo_API.txt"))

    sBabel = getBabelTerms(senses, babelInfo, False)
    
    clear_file("./output/babelList.txt")
    saveBabelNetList("./output/babelList.txt", sBabel)

    # ---------------------------------------------
    # ----      2b. AGREEMENT NELL' ANNOTAZIONE
    #       Calcoliamo nuovamente il livello di agreement nelle annotazioni, questa volta utilizzando il punteggio kappa di Cohen
    #          - Chi usa Python può utilizzare il cohen_kappa_score della libreria sklearn.metrics.
    #          - Se il gruppo di annotatori è formato da 3 componenti, calcolare la kappa di Cohen per ogni coppia e riportare la media risultante, che sarà il valore sintetico di agreement sulle annotazioni prodotte.
    # ---------------------------------------------

    c_score = getScore(clocchiatti_score)
    n_score = [i * 4 for i in getScore(nasari_score)]
    c_score_int = convert_to_int(c_score)
    n_score_int = convert_to_int(n_score)

    k= cohen_kappa_score(c_score_int, n_score_int)
    print ("Kappa Cohen score : " + str(round(k, 3)))


main()