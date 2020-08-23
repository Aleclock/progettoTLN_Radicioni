import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

#nltk.download('averaged_perceptron_tagger')

from frameSetStudent import *


"""
Allow to call the correct function based on type variable (frameName, frameElements, lexicalUnits)
Input:
    id: frame id
    el: frame elements (frame name, frame elements, lexical units)
Output:
    best WN synset
"""
def getWNSynset(id, el, type):

    if (type == 0):
        return syn_frameName(id, el)
    elif (type == 1):
        return syn_frameElements(id, el)
    elif (type == 2):
        return syn_lexicalUnits(id, el)


"""
Calculate the best WN synset of a frame name
Input: 
    id: frame id
    el: frame name
Output:
    best_sense: best WN synset
"""
def syn_frameName(id, el):
    
    if "_" in el:   # Disambiguation needed
        pos_tags = getPOS(el)
        el = getMainTerm(pos_tags)

    f  = getFrame(id)  # Context frame

    ctx_frame = preProcess(f.definition)
    synsets = wn.synsets(el)

    if (len(synsets) == 1): # Se esiste solo un synset, è per forza il migliore
        return synsets[0]
    elif (len(synsets) == 0):
        return None
    
    best_sense = None
    max_overlap = 0
    
    for s in synsets:
        ctx_synset = getSynsetContext(s)
        overlap = computeOverlap(ctx_frame, ctx_synset) + 1 
        if (overlap > max_overlap):
            max_overlap = overlap
            best_sense = s
    
    return best_sense


"""
Calculate the best WN synset of frame elements of frame
Input: 
    id: frame id
    el: frame elements
Output:
    best_sense: best WN synset
"""
def syn_frameElements(id, el):
    
    f = getFrame(id)
    ctx_frame = preProcess(f.definition)

    best_sense = None
    max_overlap = 0
    
    ctx_synset = []
    # Per ogni frame element nella lista
    """
    ctx_fe = []
    for fe in el:
        ctx_fe = list(set().union(ctx_fe,preProcess(f.FE[fe].definition))) # Aggiungo la definizione processata al contesto"""

    for fe in el:
        synsets = wn.synsets(fe)
        for s in synsets:
            #ctx_synset = list(set().union(ctx_synset,getSynsetContext(s)))
            ctx_synset = getSynsetContext(s)
            overlap = computeOverlap(ctx_frame, ctx_synset) + 1 
            if (overlap > max_overlap):
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
    
    f = getFrame(id)
    ctx_frame = preProcess(f.definition)

    ctx_lu = []

    for lu, value in el.items():   # Per ogni lexical unit del frame f
        # TODO al momento per trovare i synset prendo il nome del lu e tolgo le ultime due lettere. Non sono affatto convinto sia da fare così
        print (lu)
        synsets = wn.synsets(lu[:-2])
        #for s in synsets:



        ex = value["exemplars"]
        definition = value["definition"]

    return "ciao"


def disambiguateTerm(fname):
    f = getFrameByName(fname)
    f_LU = f.lexUnit
    print (len(f_LU))
    return "ciao"


"""
Calculate the overlap between two context
Input:
    signature: context of frame
    context: context of synset
Output:
    length of intersection
"""
def computeOverlap(signature, context):
    intersection = set(signature).intersection(set(context))
    return len(intersection)


"""
Create the context of a synset
The context include the definition and examples of synset (s) and its hypernyms, hyponyms
Input:
    s: synset
Output:
    context
"""
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
    - stopword removal
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


"""
Allow to determinate the Part-of-Speech of frame name
Input:
    sentence: name
Output:
    pos_tags: part-of-speech tags
"""
def getPOS(sentence):
    s = sentence.replace("_", " ")
    pos_tags = nltk.pos_tag(nltk.word_tokenize(s), tagset='universal')
    return pos_tags


"""
Retrieve the main term from a part-of-speech tagging
Input:
    pos: part-of-speech
Output:
    main term
"""
def getMainTerm(pos):
    for word, tag in pos:
        if tag == "VERB":
            return word
        elif tag == "NOUN":
            return word

    
"""
il contesto del frame è uguale nel caso del frame name, frame elements e lexical units
Cambia il contesto del synset

Frame name:
    trovo i synset dato il frame name e costruisco il contesto del synset
Frame element e lexical unit:
    prendo il nome del frame element e trovo i synset associati

"""