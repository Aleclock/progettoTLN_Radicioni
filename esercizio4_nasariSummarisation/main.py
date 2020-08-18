from summarization import *

# cd /Users/aleclock/Desktop/uni/TLN/radicioni/progettoTLN_Radicioni/esercizio4_nasariSummarisation


"""
__ Allow to load the article in path
Title viene inizializzato False in quanto la prima riga con carattere alfabetico (alpha) è il titolo dell'articolo. 
Se il primo carattere della riga è alfabetico e il titolo è già stato analizzato (title = True), allora si tratta della frase di un paragrafo.
Nel caso in cui il primo carattere dell'articolo non sia alfabetico, vuol dire che si tratta della fonte (inizia con #) o di uno spazio
Input: 
    path: file in input
Output: 
    text; dizionario contenente il titolo e la lista dei paragrafi del testo
"""
def loadDocument(path):

    with open(path, 'r', encoding='utf8') as file:
        text = dict()
        body = []

        title = False
        paragraphs = 0

        for line in file:
            if line[0].isalpha() or line[0] == '“':
                if not title:
                    text['[title]'] = line.lower()
                    title = True
                else:
                    paragraphs = paragraphs + 1
                    body.append(line.lower())
                    #text[paragraphs] = line.lower()
        text["[body]"] = body
    file.close()
    return text['[title]'] , text["[body]"]


"""
__ Load the nasari dictionary
Input: 
    path: file in input
Output: 
    concepts: dizionario {word: {term:score}}
"""
def loadNasari(path):
    concepts = dict()
    with open(path, 'r', encoding='utf8') as file:
        for line in file:
            line = (line.strip().lower().split(';'))
            concepts[line[1]] = [tuple(element.split("_")) for element in line[2:]]
    file.close()
    return concepts


"""
__ Initilize the summarization variables. Load the document (title, article) and start summarization function
"""
def init_summarization(document_path, nasari, compression):
    print("Starting compression of: {} by {}%".format(document_path.split("\\")[-1],compression))
    #nasari = dict_nasari_word_to_lexical()
    title, article = loadDocument(document_path)
    new_article = summarization(document_path, title,article, nasari, compression)
    #print("Numero caratteri documento finale: ",len(new_article),"\n")


def main():

    nasari = loadNasari("./nasariSubset/dd-small-nasari-15.txt")
    # TODO provare anche con Nasari grande, scaricare qui   https://goo.gl/85BubW
    
    method_score = "title"  # Altri: cue, phrase, cohesion TODO da implementare eventualmente
    #print (document["[title]"])
    #print (len(document["[body]"]))
    #for d,value in document.items():
        #print (d," °°°° " ,  value)
    
    #init_summarization("./documents/Andy-Warhol.txt", nasari, 10)
    init_summarization("./documents/Ebola-virus-disease.txt", nasari, 10)

main()