
import re
from lesk import * 
import pandas as pd
# cd /Users/aleclock/Desktop/uni/TLN/radicioni/progettoTLN_Radicioni/esercizio2_WSD


def openFile(path):
    sentences = []
    file = open(path, 'r')
    for line in file.readlines():
        keyword = re.search('\\*[^\\*]+\\*', line).group(0).strip('**').lower()
        line = re.sub('[-\\*\\n.]', '', line).lower().strip()
        sentences.append({'sentence': line, 'word': keyword})
    file.close()
    return sentences

def writeCSV(dict):
    pd.DataFrame(dict).to_csv('./output.csv', index=False)

def addTableRow(table, sentence, word, sense, newSentence):
    table.add_row([sentence,word,str(sense),newSentence])


def main():
    sentences = openFile("sentences.txt")

    output = {
        'Original sentence': [],
        'Word': [],
        'Synset': [],
        'New sentence': []
    }

    for s in sentences:
        best_sense = lesk(s['word'], s['sentence'])
        synonym = findSynonym(best_sense)
        newSentence = s['sentence'].replace(s['word'], str(synonym))
        #addTableRow(table, s['sentence'], s['word'],best_sense, newSentence)

        output["Original sentence"].append(s['sentence'])
        output["Word"].append(s['word'])
        output["Synset"].append(best_sense)
        output["New sentence"].append(newSentence)
    
    writeCSV(output)

main()