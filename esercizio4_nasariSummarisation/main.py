from summarization import *

from pathlib import Path

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

        ff = Path(path)
        print ("Initial length: " + str(len(ff.read_text(encoding='utf-8'))))

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
    concepts = {}
    """
    with open(path, 'r', encoding='utf8') as file:
        for line in file:
            line = (line.strip().lower().split(';'))
            concepts[line[1]] = [tuple(element.split("_")) for element in line[2:]]
    file.close()
    """

    # Allow to create a dictionary with the form:   nasari_word: {nasari_lexic:nasari_score}
    with open(path, 'r', encoding='utf8') as file:
        for line in file.readlines():
            tokens = line.split(";")
            lexical_dict = {}

            for token in tokens[2:]:
                token_part = token.split("_")
                if len(token_part) > 1:
                    lexical_dict[token_part[0]] = token_part[1]

            concepts[tokens[1].lower()] = lexical_dict
    file.close()

    return concepts


"""
Allow to save the summarised article in .txt located in path
Input:
    path: destination path
    name: file name
    article: content of file (summarised article)
    compressione: percent of reduction (used in file name)
"""
def saveArticle(path, name, article, compression):
    file = open(path + name + "_summ_" + str(compression) + ".txt", 'a')
    file.write(article)
    file.close()


"""
__ Initilize the summarization variables. Load the document (title, article) and start summarization function
"""
def init_summarization(document_path, ouput_path, nasari, compression):
    print("Starting compression of: {} by {}%".format(document_path.split("/")[-1],compression))
    title, article = loadDocument(document_path)
    article_summ = summarization(title, article, nasari, compression)
    saveArticle(ouput_path, document_path.split ("/")[-1], article_summ, compression)
    #print("Numero caratteri documento finale: ",len(new_article),"\n")


def main():

    nasari = loadNasari("./nasariSubset/dd-small-nasari-15.txt")
    #nasari = loadNasari("./nasariSubset/dd-nasari.txt")
    #nasari = loadNasari("./nasariSubset/dd-small-nasari-15__.txt") # Contain Bonaparte and Napoleone vectors
    
    method_score = "title"  # Altri: cue, phrase, cohesion TODO da implementare eventualmente    
    
    #init_summarization("./documents/Andy-Warhol.txt", nasari, 10)
    init_summarization("./documents/Ebola-virus-disease.txt", "./output/", nasari, 10)
    """init_summarization("./documents/Ebola-virus-disease.txt", "./output/", nasari, 20)
    init_summarization("./documents/Ebola-virus-disease.txt", "./output/", nasari, 30)

    init_summarization("./documents/Andy-Warhol.txt", "./output/", nasari, 10)
    init_summarization("./documents/Andy-Warhol.txt", "./output/", nasari, 20)
    init_summarization("./documents/Andy-Warhol.txt", "./output/", nasari, 30)

    init_summarization("./documents/Life-indoors.txt", "./output/", nasari, 10)
    init_summarization("./documents/Life-indoors.txt", "./output/", nasari, 20)
    init_summarization("./documents/Life-indoors.txt", "./output/", nasari, 30)
    
    init_summarization("./documents/Napoleon-wiki.txt", "./output/", nasari, 10)
    init_summarization("./documents/Napoleon-wiki.txt", "./output/", nasari, 20)
    init_summarization("./documents/Napoleon-wiki.txt", "./output/", nasari, 30)"""

main()