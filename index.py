
from Metrics import Metrics

import csv
from nltk.corpus import wordnet as wn

#cd /Users/aleclock/Desktop/uni/TLN/radicioni/progetto

def load_csv(path):
    couple_list = []
    with open(path, 'r') as fileCSV:
        for row in fileCSV.readlines()[1:]:
            temp = row.split(",")
            # TODO valutare se normalizzare gold_value (dividere per 10)
            gold_value = temp[2].replace('\n', '')
            couple_list.append((temp[0], temp[1], float(gold_value)))

    return couple_list

def main():
    #print(wordnet.get_version())
    couple_list  = load_csv('./WordSim353.csv')

    mm = Metrics()

    similarities = {
        'wup': [],
        'sp': [],
        'lch': []
    }

    for r in couple_list:
        ss1 = wn.synsets(r[0])
        ss2 = wn.synsets(r[0])

        sim_wup = Metrics.wuPalmerMetric(ss1, ss2)
        sim_path = Metrics.shortestPathMetric(ss1,ss2)
        sim_lc = Metrics.leakcockChodorowMetric(ss1,ss2)



main()