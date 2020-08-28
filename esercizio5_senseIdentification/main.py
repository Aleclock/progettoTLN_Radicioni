import csv

from semeval_mapper import *

# cd /Users/aleclock/Desktop/uni/TLN/radicioni/progettoTLN_Radicioni/esercizio5_senseIdentification

def saveList(path, list):
    with open(path, 'wt') as out_file:
        #tsv_writer = csv.writer(out_file, delimiter='\t')
        tsv_writer = csv.writer(out_file, delimiter='|')
        for l in list:
            tsv_writer.writerow(l)

def main():
    # ---------------------------------------------
    # ----      0. INDIVIDUAZIONE COPPIE
    # Le 50 coppie (sul totale di 500 coppie presenti nel file) sono da individuare sulla base del cognome, 
    # tramite la funzione definita nel notebook semeval_mapper.ipynb.
    # ---------------------------------------------

    coupleList = getList("Clocchiatti", "./it.test.data.txt") # Couple list
    saveList("./it.test.dataClocchiatti.tsv", coupleList)

main()