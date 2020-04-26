from Metrics import Metrics

import csv
import nltk
from nltk.corpus import wordnet as wn
import pandas as pd


# cd /Users/aleclock/Desktop/uni/TLN/radicioni/progetto_TLN_radicioni


def load_csv(path):
    couple_list = []
    with open(path, 'r') as fileCSV:
        for row in fileCSV.readlines()[1:]:
            temp = row.split(",")
            # TODO valutare se normalizzare gold_value (dividere per 10)
            gold_value = temp[2].replace('\n', '')
            couple_list.append((temp[0], temp[1], float(gold_value)))

    return couple_list

def writeCSV(dict):
    pd.DataFrame(dict).to_csv('./output.csv', index=False)


def main():
    # print(wordnet.get_version())
    couple_list = load_csv('./WordSim353.csv')

    mm = Metrics()

    similarities = {
        'Term 1': [],
        'Term 2': [],
        'wup': [],
        'sp': [],
        'lch': []
    }

    for r in couple_list:
        ss1 = wn.synsets(r[0])
        ss2 = wn.synsets(r[1])

        sim_wup = mm.wuPalmerMetric(ss1, ss2)
        #print (str(r[0]) + " , " + str(r[1]) + " ---- " + str(sim_wup) + " , " + str(sim_wupWN))
        sim_path = mm.shortestPathMetric(ss1, ss2)
        sim_lc = mm.leakcockChodorowMetric(ss1, ss2)

        similarities["Term 1"].append(r[0])
        similarities["Term 2"].append(r[1])
        similarities["wup"].append(sim_wup)
        similarities["sp"].append(sim_path)
        similarities["lch"].append(sim_lc)
    
    writeCSV(similarities)
    
    print("done")


main()
