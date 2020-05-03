
from lesk import * 
from reformatSemcor import *

import re
import pandas as pd
import xml.etree.ElementTree as ET

import numpy as np
import random

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

def readXML (path):
     #reformatSemcor("br-a01")  # Utilizzare la prima volta per formattare il corpus semcor
     root = ET.parse(path).getroot()
     sentences = [sentence for sentence in root.iter("s")]  # Variabile contenente tutti i <s> per le sentences
     return sentences
        


def main():

    # ---------------------------------------------
    # ----      PARTE 1
    # ---------------------------------------------

    """sentences = openFile("sentences.txt")

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

        output["Original sentence"].append(s['sentence'])
        output["Word"].append(s['word'])
        output["Synset"].append(best_sense)
        output["New sentence"].append(newSentence)
    
    writeCSV(output)"""

    # ---------------------------------------------
    # ----      PARTE 2
    # ---------------------------------------------

    sentences = readXML ("br-a01.xml")

    for s in sentences:
        tagged_words = [word for word in s.iter()
                            if word.get("cmd") is not "ignore" and      # Se non sbaglio "ignore" indica le parole che non devono essere taggate 
                            word.get("pos") in ['NN', 'NNS', 'NNPS']]   # In quanto si vuole prende un sostantivo  
        
        word = random.choice(tagged_words)  # Choose a random word (NOUN)
        
        word = word.text
        sentence = " ".join(word.text for word in s.iter()) 

        # TODO determinare il synset della parola (vedere notebook prof)
        # TODO su queste due variabili devo far partire l'algoritmo di Lesk

main()