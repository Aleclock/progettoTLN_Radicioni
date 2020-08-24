from frameSetStudent import *
from leskUtils import * 

import os
from prettytable import PrettyTable

# cd /Users/aleclock/Desktop/uni/TLN/radicioni/progettoTLN_Radicioni/esercizio3_FN

"""
Save the annotation in form:    type, frame_name, element, synset
"""
def annotateMapping (path, synset):
    if synset != None:
        file = open(path, 'a')
        #file.write(el + ", " + fn.frame(frame).name + ", " + str(synset) +"\n")
        for i in synset:
            file.write(i[0] + ", " + i[1] + ", " + i[2] + ", " + str(i[3]) + "\n")
        file.close()

def clear_file(path):
    os.remove(path)

def extractSynsetFromAnnotation(path):
    ann = []
    file = open(path, encoding="utf8")
    for line in file.readlines():
        if line != "":
            line_splitted = line.split(",")
            ann.append([item.strip() for item in line_splitted])
    return ann

def compareAnnotation(ann_in, ann_out):
    correct = 0
    for i in range (0, len(ann_in)):
        if ann_in[i] == ann_out[i]:
            correct += 1
    return (correct/len(ann_in))

def main ():

    #clear_file ("./ann_output.txt")

    # ---------------------------------------------
    # ----      0. INDIVIDUAZIONE DI UN SET DI FRAME
    # Come prima operazione ciascuno deve individuare un insieme di frame (nel seguito riferito come FrameSet) su cui deve lavorare.
    # La funzione restituisce, dato un cognome in input, l'elenco di frame da elaborare.
    # ---------------------------------------------

    #frameSet = getFrameSetForStudent('Clocchiatti')
    frameSet = [31, 120, 1030, 1771, 2303] # id
    
    # ---------------------------------------------
    # ----      1. ASSEGNAZIONE DI UN WN SYNSET AD UN ELEMENTO FRAMENET
    # Per ogni frame nel FrameSet è necessario assegnare un WN synset ai seguenti elementi: Frame name, Frame Elements (FEs) del frame e Lexical Units (LUs)
    # ---------------------------------------------

    table = PrettyTable()
    table.field_names = ["Frame ID", "Frame", "Synset by Frame name", "Synset by FE", "Synset by LU"]

    #for f in frameSet[:1]:
    for f in frameSet[:1]:
        f_name = getFrameName(f)
        f_FE = getFrameElements(f)
        f_LU = getFrameLU(f)

        print ("Analayzing frame: " + getFrame(f).name)
        print (getFrame(f).definition)

        #syn_fname = getWNSynset(f, f_name, 0)
        #syn_fe = getWNSynset(f, f_FE, 1)
        syb_lu = getWNSynset(f, f_LU, 2) 


        #annotateMapping ("./ann_output.txt", syn_fname)
        #annotateMapping ("./ann_output.txt", syn_fe)
        #annotateMapping ("./ann_output.txt", syb_lu)

        print ("--------------------------------------------------------------------------------")
        print ("--------------------------------------------------------------------------------")
        #table.add_row([str(f), str(f_name) , str(syn_fname), str(syn_fe), str(syb_lu)])
    
    #print(table)

    # ---------------------------------------------
    # ----      2. VALUTAZIONE DELL'OUTPUT DEL SISTEMA
    # Il programma implementato dovrà quindi fornire anche la funzionalità di valutazione, che confronterà i synset restituiti in output dal sistema 
    # con quelli annotati a mano dallo studente; su questa base deve essere calcolata l'accuratezza del sistema, 
    # semplicemente come rapporto dei corretti sul totale.
    # ---------------------------------------------
    """
    ann_in = extractSynsetFromAnnotation("./ann_input.txt")
    ann_out = extractSynsetFromAnnotation("./ann_output.txt")
    score = compareAnnotation(ann_in,ann_out)

    print ("Valutazione: " + str(score))"""

main()