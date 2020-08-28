from Metrics import Metrics
from Correlation import *

import csv
import nltk
from nltk.corpus import wordnet as wn
import pandas as pd
from prettytable import PrettyTable


# cd /Users/aleclock/Desktop/uni/TLN/radicioni/progettoTLN_Radicioni/esercizio1_ConceptSimilarity

"""
Allow to load a csv file
Input:
    path: path file
Output:
    list
"""
def load_csv(path):
    couple_list = []
    with open(path, 'r') as fileCSV:
        for row in fileCSV.readlines()[1:]:
            temp = row.split(",")
            gold_value = temp[2].replace('\n', '')
            couple_list.append((temp[0], temp[1], float(gold_value)/10))

    return couple_list

"""
Allow to write a dictionary
Input:
    dict: dictionary
"""
def writeCSV(dict):
    pd.DataFrame(dict).to_csv('./output.csv', index=False)


def main():
    # print(wordnet.get_version())
    couple_list = load_csv('./WordSim353.csv')

    mm = Metrics()

    similarities = {
        'Term 1': [],
        'Term 2': [],
        'Target': [],
        'wup': [],
        'sp': [],
        'lch': [],
        'wup_api': [],
        'sp_api': [],
        'lch_api': []
    }

    for r in couple_list[:]:
        ss1 = wn.synsets(r[0])
        ss2 = wn.synsets(r[1])

        # ------------------------------------------
        # - 0. Calcolo similarità tra parole 
        # ------------------------------------------

        sim_wup = mm.wuPalmerMetric(ss1, ss2)
        sim_path = mm.shortestPathMetric(ss1, ss2)
        sim_lc = mm.leakcockChodorowMetric(ss1, ss2)

        similarities["Term 1"].append(r[0])
        similarities["Term 2"].append(r[1])
        similarities["Target"].append(r[2])
        similarities["wup"].append(sim_wup)
        similarities["sp"].append(sim_path)
        similarities["lch"].append(sim_lc)
        similarities["wup_api"].append(mm.wuPalmerMetricAPI(ss1,ss2))
        similarities['sp_api'].append(mm.shortestPathMetricAPI(ss1, ss2))
        similarities['lch_api'].append(mm.leakcockChodorowMetricAPI(ss1, ss2))

    writeCSV(similarities)

    # ------------------------------------------
    # - 1. Calcolo indice di correlazione
    # ------------------------------------------

    table = PrettyTable()
    table.title = 'Personal - target'
    table.field_names = ["Similarity index", "Spearman index", "Pearson index"]
    table.add_row(["", "", ""])
    table.add_row(["PERSONAL / TARGET", "", ""])
    table.add_row(["", "", ""])
    table.add_row(["Wu & Palmer", pearson_index(similarities["Target"], similarities["wup"]), spearman_index(similarities["Target"], similarities["wup"])])
    table.add_row(["Shortest Path", pearson_index(similarities["Target"], similarities["sp"]), spearman_index(similarities["Target"], similarities["sp"])])
    table.add_row(["Leakcock & Chodorow", pearson_index(similarities["Target"], similarities["lch"]), spearman_index(similarities["Target"], similarities["lch"])])
    table.add_row(["", "", ""])
    table.add_row(['------------','-----------','------------'])
    table.add_row(["", "", ""])
    table.add_row(["PERSONAL / NLTK", "", ""])
    table.add_row(["", "", ""])
    table.add_row(["Wu & Palmer", pearson_index(similarities["wup"], similarities["wup_api"]), spearman_index(similarities["wup"], similarities["wup_api"])])
    table.add_row(["Shortest Path", pearson_index(similarities["sp"], similarities["sp_api"]), spearman_index(similarities["sp"], similarities["sp_api"])])
    table.add_row(["Leakcock & Chodorow", pearson_index(similarities["lch"], similarities["lch_api"]), spearman_index(similarities["lch"], similarities["lch_api"])])
    print(table)

main()
