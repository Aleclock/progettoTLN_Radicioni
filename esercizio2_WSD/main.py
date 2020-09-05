
from leskUtils import * 
from reformatSemcor import *

import re
import pandas as pd
import xml.etree.ElementTree as ET
from nltk.wsd import lesk as leskNLTK
from sklearn.metrics import accuracy_score

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

def writeCSV(dict, name):
    pd.DataFrame(dict).to_csv('./' + name + '.csv', index=False)

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
    # Disambiguare i termini polisemici all’interno delle frasi del file ‘sentences.txt’; 
    # oltre a restituire i synset ID del senso (appropriato per il contesto), il programma deve riscrivere ciascuna frase in input sostituendo 
    # il termine polisemico con l’elenco dei sinonimi eventualmente presenti nel synset.
    # ---------------------------------------------

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

        output["Original sentence"].append(s['sentence'])
        output["Word"].append(s['word'])
        output["Synset"].append(best_sense)
        output["New sentence"].append(newSentence)
    
    #writeCSV(output, "outputDisambiguation")

    # ---------------------------------------------
    # ----      PARTE 2
    # Estrarre 50 frasi dal corpus SemCor (corpus annotato con i synset di WN) e disambiguare almeno un sostantivo per frase. 
    # Calcolare l’accuratezza del sistema implementato sulla base dei sensi annotati in SemCor.
    # ---------------------------------------------

    sentences = readXML ("br-a01.xml")
    sentences = random.sample(sentences, 50)    # Vengono selezionate 50 frasi casuali

    database = {
        'Sentence': [],
        'Ambiguos term': [],
        'Semcor synset': [],
        'My synset': [],
        'Nltk synset': []
    }

    for s in sentences:
        tagged_words = [word for word in s.iter()
                            if word.get("cmd") is not "ignore" and      # "ignore" indica le parole che non devono essere taggate 
                            word.get("lexsn") is not None and
                            word.get("lemma") is not None and 
                            word.get("pos") in ['NN', 'NNS', 'NNPS'] and  # In quanto si vuole prende un sostantivo  
                            word.get("wnsn") != "0"]   

        word = random.choice(tagged_words)  # Choose a random word (NOUN)

        # http://www.nltk.org/_modules/nltk/corpus/reader/wordnet.html#WordNetCorpusReader.synset_from_sense_key
        semCorSynset = wn.synset_from_sense_key("%".join([word.get("lemma"), word.get("lexsn")]))   # Synset annotate in semCor

        w = word.text   # Word to disambiguate
        sentence = " ".join(term.text for term in s.iter()) 
        
        best_sense = lesk(w, sentence)
        best_senseNLTK = leskNLTK(sentence,w)

        database["Sentence"].append(sentence)
        database["Ambiguos term"].append(w)
        database["Semcor synset"].append(semCorSynset)
        database["My synset"].append(best_sense)
        database["Nltk synset"].append(best_senseNLTK)

    #writeCSV(database, "outputSemcor")

    ground = [str(i) for i in database["Semcor synset"]]
    predicted_lesk = [str(i) for i in database["My synset"]]
    predicted_nltk = [str(i) for i in database["Nltk synset"]]

    accuracyPersonal = accuracy_score(ground,predicted_lesk)
    accuracyNLTK = accuracy_score(ground,predicted_nltk)

    print ("------------------")
    print ("Accuracy with personal Lesk: "  + str(accuracyPersonal))
    print ("Accuracy with Nltk Lesk: "  + str(accuracyNLTK))
    print ("------------------")
main()