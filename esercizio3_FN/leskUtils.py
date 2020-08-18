import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

#nltk.download('averaged_perceptron_tagger')

from frameSetStudent import *

def getWNSynset(id, el, type):

    if (type == 0):
        return syn_frameName(id, el)
    elif (type == 1):
        return syn_frameElements(id, el)
    elif (type == 2):
        return syn_lexicalUnits(id, el)


#Determina il synset migliore dato in input il frame name
def syn_frameName(id, el):
    
    #TODO se multiword expression --> disambiguare
    if "_" in el: 
        aaa = getPOS(el)

    f  = getFrame(id)  # Context frame

    
    ctx_frame = preProcess(f.definition)
    synsets = wn.synsets(el)

    if (len(synsets) == 1): # Se esiste solo un synset, è per forza il migliore
        return synsets[0]
    
    best_sense = None
    max_overlap = 0
    
    for s in synsets:
        ctx_synset = getSynsetContext(s)
        overlap = computeOverlap(ctx_frame, ctx_synset) + 1 
        if (overlap>max_overlap):
            max_overlap = overlap
            best_sense = s
    
    return best_sense


def syn_frameElements(id, el):
    
    f = getFrame(id)

    best_sense = None
    max_overlap = 0
    
    ctx_fe = []
    ctx_synset = []
    # Per ogni frame element nella lista
    for fe in el:
        ctx_fe = list(set().union(ctx_fe,preProcess(f.FE[fe].definition))) # Aggiungo la definizione processata al contesto

    for fe in el:
        synsets = wn.synsets(fe)
        for s in synsets:
            ctx_synset = list(set().union(ctx_synset,getSynsetContext(s)))
            overlap = computeOverlap(ctx_fe, ctx_synset) + 1 
            if (overlap>max_overlap):
                max_overlap = overlap
                best_sense = s

    return best_sense

"""
Input: 
    id : id del frame
    el : dizionario contenente tutte le lexical unit
Output: 
    best_sense : WordNet synset che massimizza i contesti
"""
def syn_lexicalUnits(id, el):
    #f = getFrame(id)

    ctx_lu = []

    for lu, value in el.items():   # Per ogni lexical unit del frame f
        #print (value["ID"])
        # TODO al momento per trovare i synset prendo il nome del lu e tolgo le ultime due lettere. Non sono affatto convinto sia da fare così
        synsets = wn.synsets(lu[:-2])
        #print (synsets)
        ex = value["exemplars"]
        definition = value["definition"]

    return "ciao"

def disambiguateTerm(fname):
    f = getFrameByName(fname)
    f_LU = f.lexUnit
    print (len(f_LU))
    return "ciao"

def computeOverlap(signature, context):
    intersection = set(signature).intersection(set(context))
    return len(intersection)

def getSynsetContext(s):
    context = preProcess(s.definition())
    
    for e in s.examples():
        context = list(set().union(context,preProcess(e)))
    
    for hypernym in s.hypernyms():
        context = list(set().union(context,preProcess(hypernym.definition())))
        for e in hypernym.examples():
            context = list(set().union(context,preProcess(e)))

    for hypo in s.hyponyms():
        context = list(set().union(context,preProcess(hypo.definition())))
        for e in hypo.examples():
            context = list(set().union(context,preProcess(e)))

    return context

""" Made the pre-process of a sentence
    - stopword remuval
    - puntualization removal
    - lemmatization 
    Return a list of words"""
def preProcess(d):
    stop_words = set(stopwords.words('english'))
    punct = {',', ';', '(', ')', '{', '}', ':', '?', '!','.'}
    wnl = nltk.WordNetLemmatizer()
    ps = PorterStemmer()
    
    tokens = nltk.word_tokenize(d)
    tokens = list(filter(lambda x: x not in stop_words and x not in punct, tokens)) #and "'s" not in x
    tokens = list(set(wnl.lemmatize(t) for t in tokens))
    tokens = list(set(ps.stem(t) for t in tokens)) 
    return tokens

def getPOS(sentence):
    s = sentence.replace("_", " ")
    pos_tags = nltk.pos_tag(nltk.word_tokenize(s))
    print (pos_tags)
    return pos_tags