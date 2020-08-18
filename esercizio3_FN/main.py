from frameSetStudent import *
from leskUtils import * 

from prettytable import PrettyTable

# cd /Users/aleclock/Desktop/uni/TLN/radicioni/progettoTLN_Radicioni/esercizio3_FN
     

def main ():

    # ---------------------------------------------
    # ----      0. INDIVIDUAZIONE DI UN SET DI FRAME
    # Come prima operazione ciascuno deve individuare un insieme di frame (nel seguito riferito come FrameSet) su cui deve lavorare.
    # La funzione restituisce, dato un cognome in input, l'elenco di frame da elaborare.
    # ---------------------------------------------

    #dataset = getFrameSetForStudent('Clocchiatti')
    dataset = [31, 120, 1030, 1771, 2303]
    
    # ---------------------------------------------
    # ----      1. ASSEGNAZIONE DI UN WN SYNSET AD UN ELEMENTO FRAMENET
    # Per ogni frame nel FrameSet è necessario assegnare un WN synset ai seguenti elementi: Frame name, Frame Elements (FEs) del frame e Lexical Units (LUs)
    # ---------------------------------------------

    table = PrettyTable()
    table.field_names = ["Frame ID", "Frame", "Synset by Frame name", "Synset by FE", "Synset by LU"]

    for f in dataset[:]:
        f_name = getFrameName(f)
        f_FE = getFrameElements(f)
        f_LU = getFrameLU(f)

        syn_fname = ""
        syn_fe = ""

        syn_fname = getWNSynset(f, f_name, 0)
        #syn_fe = getWNSynset(f, f_FE, 1)
        syb_lu = getWNSynset(f, f_LU, 2)

        print ("-----")
        table.add_row([str(f), str(f_name) , str(syn_fname), str(syn_fe), syb_lu])
    
    print(table)

main()